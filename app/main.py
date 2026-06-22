from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.dashboard import router as dashboard_router
from app.webhooks.ebay import router as ebay_router
from app.webhooks.tiktok import router as tiktok_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ecommerce Order Alerts")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(dashboard_router, tags=["Dashboard"])
app.include_router(ebay_router, prefix="/webhooks/ebay", tags=["eBay"])
app.include_router(tiktok_router, prefix="/webhooks/tiktok", tags=["TikTok"])


@app.get("/health")
def health():
    return {"status": "ok"}
