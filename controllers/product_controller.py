# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.base_rest.controllers import main


class SyncProduct(http.Controller):
    @http.route('/sync_product/sync_product/', auth='public')
    def index(self, **kw):
        template = """"""
        return template
        
class SyncProductApiController(main.RestController):
    _root_path = "/sync_product_api/v1/"
    _collection_name = "base.rest.product.services"
    _default_auth = "user"

class SyncPydanticProductApiController(main.RestController):
    _root_path = "/sync_pydantic_product_api/v1/"
    _collection_name = "base.rest.pydantic.product.services"
    _default_auth = "public"

