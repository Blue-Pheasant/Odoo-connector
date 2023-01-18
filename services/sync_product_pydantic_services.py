from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_pydantic.restapi import PydanticModel, PydanticModelList
from odoo.addons.component.core import Component
from odoo.addons.base_rest.components.service import to_bool, to_int

from ..core.pydantic_sync_product import PydanticSyncProduct
from ..core.pydantic_sync_product_short import PydanticSyncProductShortInfo
from ..core.sync_product_search_param import SyncProductSearchParam


class SyncProductPydanticService(Component):
    _inherit = "base.rest.service"
    _name = "sync.product.pydantic.service"
    _usage = "sync_product_pydantic"
    _collection = "base.rest.pydantic.product.services"
    _description = """
        Product New API Services
        Services developed with the new api provided by base_rest
        Use for sync product from e-com platform
    """

    @restapi.method(
        [(["/<int:id>/get", "/<int:id>"], "GET")],
        output_param=PydanticModel(PydanticSyncProduct),
        auth="public",
    )
    def get(self, _id):
        """
        Get product's information
        """
        product = self._get(_id)
        return PydanticSyncProduct.from_orm(product)

    @restapi.method(
        [(["/", "/search"], "GET")],
        input_param=PydanticModel(SyncProductSearchParam),
        output_param=PydanticModelList(PydanticSyncProductShortInfo),
        auth="public",
    )
    def search(self, product_search_param):
        """
        Search for products
        :param product_search_param: An instance of product.search.param
        :return: List of product.short.info
        """
        domain = []
        if product_search_param.name:
            domain.append(("name", "like", product_search_param.name))
        if product_search_param.id:
            domain.append(("id", "=", product_search_param.id))
        res = []
        for p in self.env["sync.product"].sudo().search(domain):
            res.append(PydanticSyncProductShortInfo.from_orm(p))
        return res
    
    def _get(self, _id):
        return self.env["sync.product"].sudo().browse(_id)