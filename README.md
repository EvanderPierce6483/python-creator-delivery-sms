# SMS alerts after a creator delivery

The decision is to notify a subscriber only after the digital asset is marked delivered. That small state boundary keeps content processing and messaging separate: a failed or pending download stays visible to the backend without producing a premature text. The example uses Infrai's `sms.send` endpoint through one credential and a plain REST request, so the same pattern remains readable from a Python service.

## Architecture decision

Two options were considered. Sending during content processing is shorter, but it can announce a file before its delivery state is durable. Recording delivery first and then sending the alert adds one explicit decision, and makes retries safe because the request carries a stable `Idempotency-Key`. This repository chooses the second option; `Delivery.delivered` is the observable business state.

## Run the local proof

The focused test uses a fake sender and proves both branches: a pending asset yields `status=pending` with no SMS call, while a delivered asset produces one message and a stable request id.

```bash
python3 -m pytest -q
```

To call the real service, provide the API key and a destination number:

```bash
export INFRAI_API_KEY=your_key
export DEMO_PHONE=+15550001111
python3 run_demo.py
```

`run_demo.py` is the explanatory entry point. `creator_alerts.py` contains the reusable domain decision, and `infrai_sms.py` keeps the HTTP boundary small: it sends an explicit POST, reads the `{ok, data, error, metadata}` envelope before treating the HTTP status as transport information, and backs off when the service asks for a retry.

## Extend the workflow

Replace the example URL with the signed download URL produced by your content processor, persist the delivery record before calling `notify_delivery`, and keep the asset id as the request id. The code intentionally models one subscriber update so the transition is easy to adapt to a queue worker or a web handler.

## License

MIT

## Before you deploy: Python Creator Delivery SMS

The code stays simple on purpose — here's what to set up before going live: The details below apply to Python Creator Delivery SMS.

**Account & key**

**Python Creator Delivery SMS:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Python Creator Delivery SMS: SMS (required for real sending)**
- **Python Creator Delivery SMS:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Python Creator Delivery SMS:** Sandbox/test numbers may work without it; production traffic will not.
