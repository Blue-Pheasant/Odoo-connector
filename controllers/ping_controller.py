from odoo.addons.base_rest.controllers import main

class PingApiController(main.RestController):
    _root_path = "/ping/v1/"
    _collection_name = "base.rest.ping.services"
    _default_auth = "public"