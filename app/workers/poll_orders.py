import time
from app.config import settings
from app.database import SessionLocal, Base, engine
from app.services.ebay_client import EbayClient
from app.services.tiktok_client import TikTokClient
from app.services.order_service import process_order

Base.metadata.create_all(bind=engine)


def poll_once() -> None:
    db = SessionLocal()
    try:
        clients = [EbayClient(), TikTokClient()]
        for client in clients:
            for order in client.fetch_new_orders():
                result = process_order(db, order)
                print(result)
    finally:
        db.close()


def main() -> None:
    print(f"Starting order poller every {settings.poll_interval_seconds}s. Mock mode={settings.mock_mode}")
    while True:
        poll_once()
        time.sleep(settings.poll_interval_seconds)


if __name__ == "__main__":
    main()
