import json
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from ..utils.gen_uuid import _gen_uuid

from PIL import Image
from ..models.sync_order import SyncOrder

from odoo import api, fields, models
from datetime import datetime
import io
import logging
import base64
import requests
from odoo.tools import config

FIELDS_RECURSION_LIMIT = 3
ERROR_PREVIEW_BYTES = 200
DEFAULT_IMAGE_TIMEOUT = 3
DEFAULT_IMAGE_MAXBYTES = 10 * 1024 * 1024
DEFAULT_IMAGE_REGEX = r"^(?:http|https)://"
DEFAULT_IMAGE_CHUNK_SIZE = 32768

_logger = logging.getLogger(__name__)
class SyncOrderService(Component):
    _inherit = "base.rest.service"
    _name = "sync.order.service"
    _usage = "sync_order"
    _collection = "base.rest.order.services"
    _description = """
        Order New API Services
        Services developed with the new api provided by base_rest
        Use for sync order from e-com platform
    """

    def get(self, _id):
        """
        Get sync order's informations
        """
        return self._to_json(self._get(_id))

    def search(self, uniquid):
        """
        Searh sync order by uniquid
        """
        orders = self.env["sync.order"].name_search(uniquid)
        orders = self.env["sync.order"].browse([i[0] for i in orders])
        rows = []
        res = {"count": len(orders), "rows": rows}
        for sync_order in orders:
            rows.append(self._to_json(sync_order))
        return res

    def create(self, **params):
        """
        Create a new order
        """
        # sync_order = self.env["sync.order"].create(self._prepare_sync_order_params(params))
        sale_order = self.env["sale.order"].create(self._prepare_sale_order_params(params))
        # self._trigger_after_create_update(sale_order, params)
        return self._to_json(sale_order)

    def update(self, _id, **params):
        """
        Update order informations
        """
        order = self._get(_id)
        order.write(self._prepare_params(params))
        # self._trigger_after_create_update(order, params)
        return self._to_json(order)
    
    def _get(self, _id):
        return self.env["sync.order"].browse(_id)
    
    # def _trigger_after_create_update(self, order, params):
    #     if params["image_url"]:
    #         image_base_64 = self._import_image_by_url(params["image_url"])
    #         if image_base_64:
    #             is_update = order._update_image(order.id, image_base_64.decode())
    #             if not is_update:
    #                 _logger.exception("Fail to update image")

    def _get_product_from_uniquid(self, uniquid):
        result = self.env['product.product'].search([('barcode', '=', uniquid)])
        print('prodcut:', result.id)
        
        if result:
            return result.id
        return False
    
    def _get_partner_from_uniquid(self, uniquid):
        query = """
            SELECT id FROM sync_partner WHERE uniquid = '{uniquid}'
        """.format(uniquid = uniquid)

        result = self._cr.execute(query)
        print(result)

        if result:
            return result
        return False

    def _prepare_sync_order_params(self, params):
        vals = {}
        uuid = _gen_uuid()

        if uuid:
            vals["uniquid"] = uuid
        if "date_order" in params:
            date_order = fields.Datetime.now()
            if date_order:
                vals["date_order"] = date_order
        if "date_order" in params:
            vals["date_order"] = params["date_order"]
        if "product_id" in params:
            vals["product_id"] = params["product_id"]

        return vals

    def _prepare_sale_order_params(self, params):
        vals = {}
        if "date_order" in params:
            date_order = fields.Datetime.now()
            if date_order:
                vals["date_order"] = date_order

        validity_date = self._default_validity_date()
        if validity_date:
            vals["validity_date"] = validity_date
        # else: 
        #     validity_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #     if validity_date:
        #         vals["validity_date"] = validity_date

        # if params["partner_uniqid"]:
        #     partner_id = self._get_partner_from_uniquid(params["partner_uniqid"])
        #     if partner_id:
        #         vals["partner_id"] = partner_id
        # else:
        if params["partner_id"]:
            vals["partner_id"] = int(params["partner_id"])
            print("partner_id: ", params["partner_id"])
        else:
            vals["partner_id"] = 44
        if params["state"]:
            vals["state"] = params["state"]
        if params["client_order_ref"]:    
            vals["client_order_ref"] = params["client_order_ref"]
        if params["picking_policy"]:
            vals["picking_policy"] = params["picking_policy"]

        order_line = self._prepare_sale_order_line_params(params["order_line"])
        if order_line:
            vals["order_line"] = order_line

        # print(vals)
        return vals 

    # The value given for the one2many field order_line should be a list of commands.  
    # Use the command (0, 0, vals) to create a new line:
    def _prepare_sale_order_line_params(self, order_lines):
        order_line_params = []
        for order in order_lines:
            vals = {}
            
            # if order["price_unit"]:
            #     vals["price_unit"] = order["price_unit"]

            # if order["discount"]:
            #     vals["discount"] = order["discount"]

            # if order["tax_id"]:
            #     vals["tax_id"] = order["tax_id"]

            if order["product_uniquid"]:
                product_id = self._get_product_from_uniquid(order["product_uniquid"])
                if product_id:
                    vals["product_id"] = product_id
                else:
                    vals["product_id"] = 72

            if order["product_uom_qty"]:
                vals["product_uom_qty"] = order["product_uom_qty"]


            record = (0, 0, vals)
            order_line_params.append(record)

        return order_line_params

    def _default_validity_date(self):
        if self.env['ir.config_parameter'].sudo().get_param('sale.use_quotation_validity_days'):
            days = self.env.company.quotation_validity_days
            if days > 0:
                return fields.Date.to_string(datetime.now() + datetime.timedelta(days))
        return False

    def _prepare_confirmation_values(self):
        return {
            'state': 'sale',
            'date_order': fields.Datetime.now()
        }

    def _validator_return_get(self):
        res = self._validator_create()
        res.update({"id": {"type": "integer", "required": True, "empty": False}})
        return res

    def _validator_search(self):
        return {"name": {"type": "string", "nullable": False, "required": True}}

    def _validator_return_search(self):
        return {
            "count": {"type": "integer", "required": True},
            "rows": {
                "type": "list",
                "required": True,
                "schema": {"type": "dict", "schema": self._validator_return_get()},
            },
        }

    def _validator_create(self):
        # "partner_uniquid": {"type": "string", "required": True},
        # "product_uniquid":  {"type": "string", "required": True},
        res = {
            "state": {"type": "string", "required": True},
            "partner_id": {"type": "string", "required": True},
            "client_order_ref": {"type": "string", "required": False},
            "picking_policy": {"type": "string", "required": False},
            "validity_date": {"type": "string", "required": False},
            "price_unit": {"type": "float", "required": False},
            "discount": {"type": "float", "required": False},
            "tax_id": {"type": "string", "required": False},
            "order_line": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "product_uniquid": {"type": "string", "required": False},
                        "product_id":  {"type": "string", "required": True},
                        "product_uom_qty": {"type": "integer", "coerce": to_int, "nullable": False},
                    }
                }
            }
        }

        return res

    def _validator_return_create(self):
        res = {
            "id": {"type": "integer", "coerce": to_int, "required": True},
            # "uuid_transaction": {"type": "string", "required": True},
            # "uuid_partner": {"type": "string", "required": True},
            "state": {"type": "string", "required": True},
            "client_order_ref": {"type": "string", "required": False},
            "picking_policy": {"type": "string", "required": False},
            "validity_date": {"type": "string", "required": False},
            "price_unit": {"type": "float", "required": False},
            "discount": {"type": "float", "required": False},
            "tax_id": {"type": "string", "required": False},
            "require_payment": {"type": "string", "required": False},
            "amount_untaxed": {"type": "float", "required": True},
            # "amount_tax": {"type": "float", "required": True},
            "amount_total": {"type": "float", "required": True},
            # "invoice_status": {"type": "float", "required": False},
        }

        return res

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if "required" in res[key]:
                del res[key]["required"]
        return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def _validator_archive(self):
        return {}

    def _to_json(self, sale_order):
        # "uniquid": sale_order.uniquid or "",
        res = {
            "id": sale_order.id or "",
            "state": sale_order.state or "",
            "partner_id": sale_order.partner_id or "",
            "client_order_ref": sale_order.client_order_ref or "",
            "picking_policy": sale_order.picking_policy or "",
            "commitment_date": sale_order.commitment_date or "",
            "date_order": sale_order.date_order or "",
            "validity_date": sale_order.validity_date or "",
            "user_id": sale_order.user_id or "",
            "team_id": sale_order.team_id or None,
            "require_signature": sale_order.require_signature or "",
            # "require_payment": sale_order.require_payment or "",
            "amount_untaxed": sale_order.amount_untaxed or "",
            # "amount_tax": sale_order.amount_tax or "",
            "amount_total": sale_order.amount_total or "",
            "invoice_status": sale_order.invoice_status or "",
        }

        return res