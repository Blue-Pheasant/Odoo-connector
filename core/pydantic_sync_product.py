# -*- coding: utf-8 -*-

import pydantic
from .naive_orm_model import NaiveOrmModel

class PydanticSyncProduct(NaiveOrmModel):
    _name = 'sync_product.sync_product'
    _description = 'sync_product.sync_product'

    # Base Information
    name: str = None                # Name
    sale_ok: bool = None            # This product Can Be Sold (Boolean checkbox status)
    purchase_ok : bool = None       # This product Can Be Purchased (Boolean checkbox status)
    can_be_expensed : bool = None   # This Can Be Expensed (Boolean checkbox status)
    image_medium : str = None       # Insert your product image url

    # General Information
    type: str = None                # Select either product (Storable), consu (Consumable), service (service)
    category: str = None            # Your Product Category
    default_code: str = None        # Product's internal reference
    barcode: str = None             # Product barcode
    list_price: float = None        # Sales Price
    standard_price: float = None    # Cost price of the product
    description: str = None         # Internal Notes
    
    # Sales
    available_in_pos: bool = None   # This product will shown and can be sold in PoS (Boolean checkbox)
    to_weight: bool = None          # Check if the product should be weighted using the hardware scale integration
    invoicing_policy : str = None   # Select either "order" or "delivery"
    expense_policy : bool = None    # Select either "no", "cost", or "sales_price"

    # Inventory
    sale_delay: float = None        # Customer Lead Time
    weight: float = None            # Weight in KG
    volume: float = None            # Volume in m³