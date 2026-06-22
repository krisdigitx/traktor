from datetime import datetime
from app.config import settings
from app.schemas import IncomingOrder


class EbayClient:
    def fetch_new_orders(self) -> list[IncomingOrder]:
        if settings.mock_mode:
            minute_bucket = datetime.utcnow().strftime("%Y%m%d%H%M")
            return [IncomingOrder(
                platform="EBAY",
                shop_name="saberjmk",
                external_order_id=f"MOCK-EBAY-{minute_bucket}",
                buyer_name="eBay Buyer",
                item_title="USB-C 100W Magnetic Cable",
                quantity=1,
                currency="GBP",
                total_amount=9.99,
                status="PAID",
                raw_payload={"mock": True},
            )]

        # TODO: Implement OAuth refresh and Sell Fulfillment API /sell/fulfillment/v1/order.
        # Keep this method returning normalized IncomingOrder objects.
        return []
