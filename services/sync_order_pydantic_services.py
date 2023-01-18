from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_pydantic.restapi import PydanticModel, PydanticModelList
from odoo.addons.component.core import Component
from odoo.addons.base_rest.components.service import to_bool, to_int

from ..core.pydantic_sync_order import PydanticSyncOrder
from ..core.sync_order_search_param import SyncOrderSearchParam

class SyncOrderPydanticService(Component):
    _inherit = "base.rest.service"
    _name = "sync.order.pydantic.service"
    _usage = "sync_order_pydantic"
    _collection = "base.rest.pydantic.order.services"
    _description = """
        Order New API Services
        Services developed with the new api provided by base_rest
        Use for sync order from e-com platform
    """

    @restapi.method(
        [(["/<int:id>/get", "/<int:id>"], "GET")],
        output_param=PydanticModel(PydanticSyncOrder),
        auth="public",
    )
    def get(self, _id):
        """
        Get order's information
        """
        order = self._get(_id)
        return PydanticSyncOrder.from_orm(order)

    @restapi.method(
        [(["/", "/search"], "GET")],
        input_param=PydanticModel(SyncOrderSearchParam),
        output_param=PydanticModelList(PydanticSyncOrder),
        auth="public",
    )
    def search(self, order_search_param):
        """
        Search for orders
        :param order_search_param: An instance of order.search.param
        :return: List of order.short.info
        """
        domain = []
        if order_search_param.name:
            domain.append(("name", "like", order_search_param.name))
        if order_search_param.id:
            domain.append(("id", "=", order_search_param.id))
        res = []
        for p in self.env["sync.order"].sudo().search(domain):
            res.append(PydanticSyncOrder.from_orm(p))
        return res
    
    def _get(self, _id):
        return self.env["sync.order"].sudo().browse(_id)