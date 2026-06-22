from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import IncomingOrder
from app.services.order_service import process_order

router = APIRouter()


@router.post("/order")
async def tiktok_order_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    data = payload.get("data", payload)
    order = IncomingOrder(
        platform="TIKTOK",
        shop_name=data.get("shop_name", "TikTok UK"),
        external_order_id=str(data.get("order_id") or data.get("orderId") or data.get("id")),
        buyer_name=data.get("buyer_name"),
        item_title=data.get("item_title") or data.get("title"),
        quantity=int(data.get("quantity", 1)),
        currency=data.get("currency", "GBP"),
        total_amount=float(data.get("total_amount", data.get("total", 0)) or 0),
        status=data.get("status", "PAID"),
        raw_payload=payload,
    )
    return process_order(db, order)
