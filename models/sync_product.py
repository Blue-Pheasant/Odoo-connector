# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class SyncProduct(models.Model):
    _name = 'sync.product'
    _description = 'Sync product model'


    # Base Information
    name = fields.Char('Product name', required=True)
    uuid = fields.Char('Uniquid', required=True)
    sale_ok = fields.Boolean('Can be sold', required=True)
    purchase_ok = fields.Boolean('Can be purchased', required=True)
    can_be_expensed = fields.Boolean('Can be expensed', required=False)
    image_product = fields.Binary(string="Image", store=True, attachment=False)
    image_url = fields.Text('Product image url', help="Product image url", required=False)
    store_id = fields.Char('Sync product from store', require=True)

    # General Information
    type = fields.Char('Product type', required=True)
    category = fields.Char('Product category', required=True)
    default_code = fields.Char('Product\'s internal reference', required=False)
    barcode = fields.Char('Product\'s barcode', required=False)
    list_price = fields.Float('Sales Price', required=False)
    standard_price = fields.Float('Cost price', required=False)
    description = fields.Text('Internal Notes', required=False)
    
    # Sales
    available_in_pos = fields.Boolean('Can be sold in PoS', required=False)
    to_weight = fields.Boolean('Can be weighted', required=False)
    invoicing_policy = fields.Char('Select either order or delivery', require=False)
    expense_policy  = fields.Boolean('Select either no, cost, or sales price', required=False)

    # Inventory
    sale_delay = fields.Float('Customer Lead Time', require=False)
    weight = fields.Float('Weight in KG', require=False)
    volume = fields.Float('Volume in m³', require=False)

    # Status
    work_flow_state = fields.Char('Status of sync product', default='Unaccept', require=False)

    def _update_image(self, id, image_product):
        if not self.ids:
            return None

        query = """
            UPDATE sync_product SET image_product = '{base_64}'  WHERE id = '{id}'
        """.format(base_64 = image_product, id = id)

        result = self._cr.execute(query)

        return result