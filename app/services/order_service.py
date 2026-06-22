import json
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import Order
from app.schemas import IncomingOrder
from app.services.whatsapp_client import WhatsAppClient


def build_order_message(order: Order) -> str:
    return (
        f"🛒 New {order.platform} Order\n\n"
        f"Shop: {order.shop_name or '-'}\n"
        f"Order ID: {order.external_order_id}\n"
        f"Buyer: {order.buyer_name or '-'}\n"
        f"Item: {order.item_title or '-'}\n"
        f"Qty: {order.quantity}\n"
        f"Total: {order.currency} {order.total_amount:.2f}\n"
        f"Status: {order.status}\n"
        f"Action: Dispatch required"
    )


def create_order_if_new(db: Session, incoming: IncomingOrder) -> tuple[Order, bool]:
    order = Order(
        platform=incoming.platform.upper(),
        shop_name=incoming.shop_name,
        external_order_id=incoming.external_order_id,
        buyer_name=incoming.buyer_name,
        item_title=incoming.item_title,
        quantity=incoming.quantity,
        currency=incoming.currency,
        total_amount=incoming.total_amount,
        status=incoming.status,
        raw_payload=json.dumps(incoming.raw_payload or {}, default=str),
    )
    db.add(order)
    try:
        db.commit()
        db.refresh(order)
        return order, True
    except IntegrityError:
        db.rollback()
        existing = db.query(Order).filter_by(
            platform=incoming.platform.upper(),
            external_order_id=incoming.external_order_id,
        ).first()
        return existing, False


def notify_order(db: Session, order: Order) -> None:
    try:
        WhatsAppClient().send(build_order_message(order))
        order.notification_status = "SENT"
    except Exception as exc:
        order.notification_status = f"FAILED: {exc}"[:64]
    db.add(order)
    db.commit()


def process_order(db: Session, incoming: IncomingOrder) -> dict:
    order, is_new = create_order_if_new(db, incoming)
    if is_new:
        notify_order(db, order)
        return {"status": "new_order_processed", "order_id": order.external_order_id}
    return {"status": "already_processed", "order_id": order.external_order_id}
