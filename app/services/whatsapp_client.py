from app.config import settings


class WhatsAppClient:
    def __init__(self):
        self.enabled = bool(settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_whatsapp_from)
        self.recipients = [x.strip() for x in settings.whatsapp_alert_numbers.split(",") if x.strip()]

    def send(self, body: str) -> list[dict]:
        if not self.enabled or not self.recipients:
            print("WhatsApp not configured. Message would be:")
            print(body)
            return [{"status": "mocked", "to": "console"}]

        from twilio.rest import Client

        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        results = []
        for number in self.recipients:
            msg = client.messages.create(
                from_=f"whatsapp:{settings.twilio_whatsapp_from}",
                to=f"whatsapp:{number}",
                body=body,
            )
            results.append({"status": msg.status, "sid": msg.sid, "to": number})
        return results
