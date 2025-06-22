# pySMSGateway

**pySMSGateway** is an asynchronous Python microservice that interacts with a GSM modem using [Gammu](https://wammu.eu/gammu/). It provides a REST API for sending and receiving SMS messages and retrieving real-time modem and network details such as IMEI, signal quality, and carrier name. Incoming SMS messages can optionally be forwarded to any external service via a configurable webhook.

---

## 🚀 Features

- 📤 Send SMS via REST API  
- 📥 Receive and decode incoming SMS messages  
- 📶 Query modem details (IMEI, model, firmware, signal, operator, etc.)  
- 🔁 Poll modem periodically for new messages  
- 🔧 Easily integrates with automation, IoT, or monitoring systems  

---

## ⚙️ Configuration

Set the following environment variables to configure the gateway:

| Variable           | Description                                                        | Default                             |
|--------------------|--------------------------------------------------------------------|-------------------------------------|
| `WEBHOOK_URL`      | URL to forward incoming SMS as a JSON payload (optional)           | `http://localhost:8123/webhook/sms` |
| `WEBHOOK_TOKEN`    | Optional bearer token for secure webhook POSTs                     | —                                   |
| `GSM_DEVICE`       | Path to GSM modem serial port (e.g. `/dev/ttyUSB0`)                | `/dev/ttyUSB0`                      |
| `GSM_CONNECTION`   | Modem connection string (e.g. `at19200`, `at115200`)               | `at115200`                          |
| `POLL_INTERVAL`    | Interval (seconds) to poll modem for new messages                  | `10`                                |

---

## 📡 API Endpoints

### `POST /api/sms/send`

Send an SMS message via modem.

**Request**:

```json
{
  "number": "+15551234567",
  "text": "Hello from pySMSGateway!"
}
```

**Response**:

```json
{ "status": "SMS sent" }
```

---

### `GET /api/sms/info`

Retrieve modem metadata and network diagnostics.

**Response**:

```json
{
  "manufacturer": "Quectel",
  "model": "EC25",
  "firmware": "01.000.01.001",
  "imei": "867322032XXXXX",
  "signal_quality": { "SignalStrength": 21, "SignalPercent": 55 },
  "network_info": {
    "NetworkCode": "310260",
    "NetworkName": "T-Mobile",
    "LAC": "0001",
    "CID": "0A2B"
  }
}
```

---

## 🔁 Webhook Forwarding

When an incoming SMS is received, a `POST` request is sent to your `WEBHOOK_URL` containing:

```json
{
  "phone": "+15559876543",
  "date": "2025-06-22 11:30:00",
  "message": "Your gateway is working!"
}
```

The `Authorization: Bearer WEBHOOK_TOKEN` header is included if configured.

---

## 🐳 Running via Docker

```bash
docker build -t pysmsgateway .
docker run --rm -it \
  -e GSM_DEVICE=/dev/ttyUSB0 \
  -e GSM_CONNECTION=at115200 \
  -e WEBHOOK_URL=https://your-service.example.com/sms \
  -e WEBHOOK_TOKEN=your-secret-token \
  --device=/dev/ttyUSB0 \
  -p 3000:3000 \
  pysmsgateway
```

---

## 🛠️ Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # include aiohttp, python-gammu, etc.
python sms_gateway.py
```

---

## 📝 License

MIT License

---

## 🤝 Contributing

Bug reports, feature suggestions, and pull requests are welcome!
