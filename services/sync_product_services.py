import json
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from PIL import Image
from ..models.sync_product import SyncProduct

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
class SyncProductService(Component):
    _inherit = "base.rest.service"
    _name = "sync.product.service"
    _usage = "sync_product"
    _collection = "base.rest.product.services"
    _description = """
        Product New API Services
        Services developed with the new api provided by base_rest
        Use for sync product from e-com platform
    """

    def get(self, _uuid):
        """
        Get sync product's informations by uuid
        """
        return self._to_json(self._get(_uuid))

    def search(self, name):
        """
        Searh sync product by name
        """
        products = self.env["sync.product"].name_search(name)
        products = self.env["sync.product"].browse([i[0] for i in products])
        rows = []
        res = {"count": len(products), "rows": rows}
        for sync_product in products:
            rows.append(self._to_json(sync_product))
        return res

    def create(self, **params):
        """
        Create a new product
        """
        product = self.env["sync.product"].create(self._prepare_params(params))
        self._trigger_after_create_update(product, params)
        return self._to_json(product)

    def update(self, _uuid, **params):
        """
        Update product informations
        """
        product = self._get(_uuid)
        product.write(self._prepare_params(params))
        self._trigger_after_create_update(product, params)
        return self._to_json(product)
    
    def _trigger_after_create_update(self, product, params):
        if params["image_url"]:
            image_base_64 = self._import_image_by_url(params["image_url"])
            if image_base_64:
                is_update = product._update_image(product.id, image_base_64.decode())
                if not is_update:
                    _logger.exception("Fail to update image")

    def _get(self, _uuid):
        sync_product = self.env['sync.product'].search([('uuid', '=', _uuid)])
        return sync_product

    def _prepare_params(self, params):
        return params

    # Validator
    def _validator_return_get(self):
        res = {
            "name": {"type": "string", "required": True},
            "uuid": {"type": "string", "required": True},
            "sale_ok": {"coerce": to_bool, "type": "boolean", "required": True},
            "purchase_ok": {"coerce": to_bool, "type": "boolean", "required": False},
            "can_be_expensed": {"coerce": to_bool, "type": "boolean", "required": False},
            "image_url": {"type": "string", "required": False},
            "store_id": {"type": "string", "required": True},
            "category": {"type": "string", "required": True},
            "type": {"type": "string", "required": True},
            "default_code": {"type": "string", "nullable": True},
            "barcode": {"type": "string", "nullable": True},
            "list_price": {"type": "float", "required": True},
            "standard_price": {"type": "float", "required": False, "nullable": True},
            "available_in_pos": {"coerce": to_bool, "type": "boolean", "required": False},
            "to_weight": {"coerce": to_bool, "type": "boolean", "required": False},
            "invoicing_policy": {"coerce": to_bool, "type": "boolean", "required": False},
            "expense_policy": {"coerce": to_bool, "type": "boolean", "required": False},
            "sale_delay": {"type": "string", "nullable": True, "required": False},
            "weight": {"type": "float", "nullable": True, "required": False},
            "volume": {"type": "float", "nullable": True, "required": False},
        }
        
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

        res = {
            "name": {"type": "string", "required": True},
            "uuid": {"type": "string", "required": True},
            "sale_ok": {"coerce": to_bool, "type": "boolean", "required": True},
            "purchase_ok": {"coerce": to_bool, "type": "boolean", "required": False},
            "can_be_expensed": {"coerce": to_bool, "type": "boolean", "required": False},
            "image_url": {"type": "string", "required": False},
            "image_product": {"type": "string", "required": False},
            "store_id": {"type": "string", "required": True},
            "category": {"type": "string", "required": True},
            "type": {"type": "string", "required": True},
            "default_code": {"type": "string", "nullable": True},
            "barcode": {"type": "string", "nullable": True},
            "list_price": {"type": "float", "required": True},
            "standard_price": {"type": "float", "required": False, "nullable": True},
            "available_in_pos": {"coerce": to_bool, "type": "boolean", "required": False},
            "to_weight": {"coerce": to_bool, "type": "boolean", "required": False},
            "invoicing_policy": {"coerce": to_bool, "type": "boolean", "required": False},
            "expense_policy": {"coerce": to_bool, "type": "boolean", "required": False},
            "sale_delay": {"type": "string", "nullable": True, "required": False},
            "weight": {"type": "float", "nullable": True, "required": False},
            "volume": {"type": "float", "nullable": True, "required": False},
        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()

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

    def _to_json(self, product):
        res = {
            "id": product.id or "",
            "name": product.name or "",
            "uuid": product.uuid or "",
            "sale_ok": product.sale_ok or "",
            "purchase_ok": product.purchase_ok or "",
            "can_be_expensed": product.can_be_expensed or "",
            "image_product": product.image_product or "",
            "image_url": product.image_url or "",
            "store_id": product.store_id or "",
            "category": product.category or "",
            "type": product.type or "",
            "default_code": product.default_code or "",
            "barcode": product.barcode or "",
            "list_price": product.list_price or "",
            "standard_price": product.standard_price or None,
            "available_in_pos": product.available_in_pos or "",
            "to_weight": product.to_weight or "",
            "invoicing_policy": product.invoicing_policy or "",
            "expense_policy": product.expense_policy or "",
            "sale_delay": product.sale_delay or "",
            "weight": product.weight or "",
            "volume": product.volume  or "",
            "work_flow_state": product.work_flow_state or False
        }

        return res
    
    def _import_image_by_url(self, url):
        """ Imports an image by URL
        """
        maxsize = int(config.get("import_image_maxbytes", DEFAULT_IMAGE_MAXBYTES))
        _logger.debug("Trying to import image from URL: %s" % (url))
        try:
            response = requests.get(url, timeout=int(config.get("import_image_timeout", DEFAULT_IMAGE_TIMEOUT)))
            response.raise_for_status()

            if response.headers.get('Content-Length') and int(response.headers['Content-Length']) > maxsize:
                raise ValueError(("File size exceeds configured maximum (%s bytes)", maxsize))

            content = bytearray()
            for chunk in response.iter_content(DEFAULT_IMAGE_CHUNK_SIZE):
                content += chunk
                if len(content) > maxsize:
                    raise ValueError(("File size exceeds configured maximum (%s bytes)", maxsize))

            image = Image.open(io.BytesIO(content))
            w, h = image.size
            if w * h > 42e6:  # Nokia Lumia 1020 photo resolution
                raise ValueError(
                    u"Image size excessive, imported images must be smaller "
                    u"than 42 million pixel")

            return base64.b64encode(content)
        except Exception as e:
            _logger.exception(e)
            raise ValueError(("Could not retrieve URL: %(url)s %(error)s") % {
                'url': url,
                'error': e
            })

