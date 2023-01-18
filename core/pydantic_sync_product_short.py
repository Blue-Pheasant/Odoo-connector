# -*- coding: utf-8 -*-

import pydantic
from .naive_orm_model import NaiveOrmModel
class PydanticSyncProductShortInfo(NaiveOrmModel):
    _name = 'sync_product.sync_product'
    _description = 'sync_product.sync_product'

    # Base Information
    name: str                       # Name
    sale_ok: bool                   # This product Can Be Sold (Boolean checkbox status)
    purchase_ok : bool              # This product Can Be Purchased (Boolean checkbox status)
    image_medium : str = None       # Insert your product image url
    type: str                       # Select either product (Storable), consu (Consumable), service (service)
    category: str = None            # Your Product Category
    list_price: float               # Sales Price
    description: str = None         # Internal Notes

    # Inventory
    sale_delay: float = None        # Customer Lead Time
    weight: float = None            # Weight in KG
    volume: float = None            # Volume in m³