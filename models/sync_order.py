# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import datetime

class SyncOrder(models.Model):
    _name = 'sync_order.sync_order'
    _description = 'sync_order.sync_order'

    uniquid = fields.Char('Product identifier', required=True, help='This uniquid is required for ident customer from another e-com platfrom')
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, default=fields.Datetime.now, 
                                help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    partner_id = fields.Char(string='Partner identifier', required=False)
    product_id = fields.Char(string='Product identifier', required=False)

    
