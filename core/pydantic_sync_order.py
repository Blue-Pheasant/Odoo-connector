# -*- coding: utf-8 -*-

import pydantic
from .naive_orm_model import NaiveOrmModel
class PydanticSyncOrder(NaiveOrmModel):
    _name = 'sync_order.sync_order'
    _description = 'sync_order.sync_order'

    # Base Information
    state: str = None               # Status ("sent", "sale", "done", "cancel")
    uniquid: str                    # Order uniquid id -> can be checked by customer
    ordered_at: str                 # Time recognize
    partner_phone: str = None       # Customer phone number
    method_payment: str = None      # Method payment (can be ship-code or cash)
    date_order: str                 # Date time
    validity_date: str              # Date time
    picking_policy: str             # Select ("direct" or "one")
      
    # Customer information
    partner_id: str                 # Customer id

    # Product information
    product_id: str = None          # Product identitfy number
    quantity: int = None            # Quantity
    note: str = None                # Note for order
    total_price: float = None       # Total price

    # Inventory information
    weight: float = None            # Weight in KG
    volume: float = None            # Volume in m³