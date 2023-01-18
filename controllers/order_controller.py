from odoo import http
from odoo.addons.base_rest.controllers import main

class SyncOrder(http.Controller):
    @http.route('/sync_order/sync_order/', auth='public')
    def index(self, **kw):
        template = """"""
        return template

class SyncOrderApiController(main.RestController):
    _root_path = "/sync_order_api/v1/"
    _collection_name = "base.rest.order.services"
    _default_auth = "user"

class SyncPydanticOrderApiController(main.RestController):
    _root_path = "/sync_pydantic_order_api/v1/"
    _collection_name = "base.rest.pydantic.order.services"
    _default_auth = "public"
