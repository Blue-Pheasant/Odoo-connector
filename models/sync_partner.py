# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class SyncPartner(models.Model):
    _name = 'sync_partner.sync_partner'
    _description = 'sync_partner.sync_partner'

    street = fields.Char('Wards/Street', required=True)
    street2 = fields.Char('District/Hometown', required=False)
    zip_code = fields.Char('Zip code', required=True)
    city = fields.Char('Provide/City', required=True)
    phone = fields.Char('Phone number', required=False)
    email = fields.Char('Email', required=False)
    display_name = fields.Char('Display name', require=True)
    website = fields.Char('Website', required=False)
    function = fields.Char('Function', require=False)
    is_company = fields.Boolean('Is company', required=False, default=False)
    commercial_company_name = fields.Char(required=False)
    uniquid = fields.Char('Partner identifier', required=True,
                        help='This uniquid is required for ident customer from another e-com platfrom')
    