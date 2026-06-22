from datetime import datetime
from app.config import settings
from app.schemas import IncomingOrder


class TikTokClient:
    def fetch_new_orders(self) -> list[IncomingOrder]:
        if settings.mock_mode:
            minute_bucket = datetime.utcnow().strftime("%Y%m%d%H%M")
            return [IncomingOrder(
                platform="TIKTOK",
                shop_name="Tauri Royale",
                external_order_id=f"MOCK-TIKTOK-{minute_bucket}",
                buyer_name="TikTok Buyer",
                item_title="Sample TikTok Shop Product",
                quantity=1,
                currency="GBP",
                total_amount=12.49,
                status="PAID",
                raw_payload={"mock": True},
            )]

        # TODO: Implement TikTok Shop order search/list endpoint with signing.
        # Keep this method returning normalized IncomingOrder objects.
        return []
