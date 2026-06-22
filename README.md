# Ecommerce Order Alerts

Python FastAPI application for TikTok UK and eBay order monitoring with WhatsApp notifications and a dashboard. It is designed for Kubernetes and ArgoCD GitOps deployment.

## What this includes

- FastAPI dashboard at `/`
- Webhook endpoints:
  - `/webhooks/ebay/order`
  - `/webhooks/tiktok/order`
- Background order polling worker
- PostgreSQL order database
- Redis placeholder for future queue support
- Twilio WhatsApp notification service
- Dockerfile
- Docker Compose local environment
- Kubernetes manifests
- ArgoCD `Application`
- GitHub Actions workflow to build and push image to GHCR

## Important WhatsApp note

The official WhatsApp Business API normally sends to individual WhatsApp users, not ordinary personal WhatsApp groups. This app supports sending the same alert to multiple WhatsApp numbers. For a real group workflow, consider Twilio Conversations, Telegram, Slack, or Discord.

## Local test

```bash
cp .env.example .env

docker compose up --build
```

Open:

```text
http://localhost:8000/
```

The app starts in `MOCK_MODE=true`, so the worker generates mock eBay and TikTok orders every polling interval and prints WhatsApp messages if Twilio is not configured.

## Manual webhook test

```bash
curl -X POST http://localhost:8000/webhooks/ebay/order \
  -H 'Content-Type: application/json' \
  -d '{
    "orderId": "EBAY-1001",
    "shop_name": "saberjmk",
    "item_title": "USB-C 100W Magnetic Cable",
    "quantity": 2,
    "currency": "GBP",
    "total": 14.98,
    "status": "PAID"
  }'
```

```bash
curl -X POST http://localhost:8000/webhooks/tiktok/order \
  -H 'Content-Type: application/json' \
  -d '{
    "data": {
      "order_id": "TIKTOK-1001",
      "shop_name": "Tauri Royale",
      "item_title": "Sample Product",
      "quantity": 1,
      "currency": "GBP",
      "total_amount": 12.49,
      "status": "PAID"
    }
  }'
```

## Configure Twilio WhatsApp

Update `.env` or Kubernetes secret:

```env
TWILIO_ACCOUNT_SID=xxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_WHATSAPP_FROM=+14155238886
WHATSAPP_ALERT_NUMBERS=+447000000000,+447111111111
```

Each number must be authorised according to your Twilio WhatsApp setup. For production, use your approved WhatsApp sender.


## Docker Hub image build

The GitHub Actions workflow pushes to Docker Hub. Create these repository secrets in GitHub:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

Create a Docker Hub access token from your Docker Hub account security settings and use it as `DOCKERHUB_TOKEN`. The image pushed by the workflow will be:

```text
docker.io/<your-dockerhub-username>/ecommerce-order-alerts:latest
```

## Kubernetes deployment

Update image names in:

```text
k8s/deployment-api.yaml
k8s/deployment-worker.yaml
```

Replace:

```text
docker.io/YOUR_DOCKERHUB_USERNAME/ecommerce-order-alerts:latest
```

with your actual Docker Hub image, for example:

```text
docker.io/raj/ecommerce-order-alerts:latest
```

Then apply directly for testing:

```bash
kubectl apply -f k8s/
```

Check pods:

```bash
kubectl get pods -n ecommerce-alerts
kubectl logs -n ecommerce-alerts deploy/order-alert-worker
kubectl port-forward -n ecommerce-alerts svc/order-alert-api 8000:80
```

Open:

```text
http://localhost:8000/
```

## ArgoCD deployment

Edit:

```text
argocd/application.yaml
```

Set your GitHub repo URL:

```yaml
repoURL: https://github.com/YOUR_GITHUB_USER/ecommerce-order-alerts.git
```

Apply:

```bash
kubectl apply -f argocd/application.yaml
```

## Production changes needed

Before going live:

1. Set `MOCK_MODE=false`.
2. Implement actual eBay OAuth refresh in `app/services/ebay_client.py`.
3. Implement TikTok Shop API signing in `app/services/tiktok_client.py`.
4. Replace `k8s/postgres.yaml` `emptyDir` with a PersistentVolumeClaim or managed PostgreSQL.
5. Use Sealed Secrets, SOPS, or External Secrets instead of committing raw secrets.
6. Add authentication to the dashboard before exposing it publicly.
7. Add HTTPS ingress with cert-manager.

## Next development tasks

- eBay Sell Fulfillment API integration
- eBay Notification API subscription validation
- TikTok Shop order API integration
- Dashboard login
- Dispatch SLA alerts
- Daily sales summary notification
- Profit calculation per order
- VA activity view
