from pydantic import BaseModel
from typing import Any, Optional


class IncomingOrder(BaseModel):
    platform: str
    shop_name: Optional[str] = None
    external_order_id: str
    buyer_name: Optional[str] = None
    item_title: Optional[str] = None
    quantity: int = 1
    currency: str = "GBP"
    total_amount: float = 0.0
    status: str = "NEW"
    raw_payload: Optional[dict[str, Any]] = None
