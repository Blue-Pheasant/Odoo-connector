# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class AcceptSyncProduct(models.TransientModel):
    _name = "accept.sync.product"
    _description = "Batch accept for create product model"

    # Base Information
    name = fields.Char('Product name', required=False)
    sale_ok = fields.Boolean('Can be sold', required=False)
    purchase_ok = fields.Boolean('Can be purchased', required=False)
    can_be_expensed = fields.Boolean('Can be expensed', required=False)
    image_product = fields.Binary('Product image', attachment=True, help="Product image", required=False)
    store_id = fields.Char('Sync product from store', require=False)

    # General Information
    type = fields.Char('Product type', required=False)
    category = fields.Char('Product category', required=False)
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

    def _prepare_product_values(self, sync_product):
        product_vals = {}

        product_vals["name"] = sync_product.name
        product_vals["sale_ok"] = sync_product.sale_ok
        product_vals["purchase_ok"] = sync_product.purchase_ok
        product_vals["type"] = sync_product.type
        # product_vals["category"] = sync_product.category
        # product_vals["categ_id"] = "All / Consumable"
        # product_vals["description"] = "sync_product.description"
        if sync_product.image_product:
            product_vals["image_1920"] = sync_product.image_product
        if sync_product.default_code:
            product_vals["default_code"] = sync_product.default_code
        if sync_product.list_price > 0:
            product_vals["list_price"] = sync_product.list_price
        if sync_product.standard_price:
            product_vals["standard_price"] = sync_product.standard_price
        if sync_product.description:
            product_vals["description"] = sync_product.description
        if sync_product.available_in_pos:
            product_vals["available_in_pos"] = sync_product.available_in_pos
        if sync_product.invoicing_policy:
            product_vals["invoicing_policy"] = sync_product.invoicing_policy
        if sync_product.expense_policy:
            product_vals["expense_policy"] = sync_product.expense_policy
        if sync_product.sale_delay > 0:
            product_vals["sale_delay"] = sync_product.sale_delay
        if sync_product.weight > 0:
            product_vals["weight"] = sync_product.weight
        if sync_product.volume > 0:
            product_vals["volume"] = sync_product.volume
        if sync_product["barcode"]:
            product_vals["barcode"] = sync_product.barcode

        return product_vals

    def _create_product(self, sync_product):
        product_vals = self._prepare_product_values(sync_product)
        sync_product.update({"work_flow_state": "Accepted"})
        product = self.env['product.template'].sudo().create(product_vals).with_user(self.env.uid)
        
        return product


    def create_products(self):
        ids = self.env.context['active_ids'] # selected record ids
        sync_products = self.env['sync.product'].browse(self._context.get('active_ids', []))
        for record in sync_products:
            if record.work_flow_state == "Unaccept":
                self._create_product(record)
                
        return {'type': 'ir.actions.act_window_close'}