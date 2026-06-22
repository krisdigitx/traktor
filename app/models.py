from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, UniqueConstraint
from app.database import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("platform", "external_order_id", name="uq_platform_order"),)

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(32), nullable=False, index=True)
    shop_name = Column(String(128), nullable=True)
    external_order_id = Column(String(128), nullable=False, index=True)
    buyer_name = Column(String(256), nullable=True)
    item_title = Column(String(512), nullable=True)
    quantity = Column(Integer, default=1)
    currency = Column(String(8), default="GBP")
    total_amount = Column(Float, default=0.0)
    status = Column(String(64), default="NEW")
    notification_status = Column(String(64), default="PENDING")
    raw_payload = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
