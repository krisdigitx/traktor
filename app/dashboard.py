from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = datetime.utcnow() - timedelta(days=7)

    total_today = db.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(Order.created_at >= today_start).scalar()
    total_week = db.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(Order.created_at >= week_start).scalar()
    count_today = db.query(Order).filter(Order.created_at >= today_start).count()
    pending_dispatch = db.query(Order).filter(Order.status.in_(["PAID", "NEW"])).count()
    failed_notifications = db.query(Order).filter(Order.notification_status.like("FAILED%" )).count()
    orders = db.query(Order).order_by(Order.created_at.desc()).limit(50).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "orders": orders,
        "count_today": count_today,
        "pending_dispatch": pending_dispatch,
        "failed_notifications": failed_notifications,
        "total_today": total_today,
        "total_week": total_week,
    })
