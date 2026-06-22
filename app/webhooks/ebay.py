from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import IncomingOrder
from app.services.order_service import process_order

router = APIRouter()


@router.post("/order")
async def ebay_order_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    # Normalize this once your eBay notification payload is confirmed.
    order = IncomingOrder(
        platform="EBAY",
        shop_name=payload.get("shop_name", "eBay UK"),
        external_order_id=str(payload.get("orderId") or payload.get("notification", {}).get("orderId") or payload.get("id")),
        buyer_name=payload.get("buyer", {}).get("username") if isinstance(payload.get("buyer"), dict) else None,
        item_title=payload.get("item_title") or payload.get("title"),
        quantity=int(payload.get("quantity", 1)),
        currency=payload.get("currency", "GBP"),
        total_amount=float(payload.get("total", 0) or 0),
        status=payload.get("status", "PAID"),
        raw_payload=payload,
    )
    return process_order(db, order)
