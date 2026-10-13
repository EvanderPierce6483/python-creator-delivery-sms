from creator_alerts import Delivery, notify_delivery


def test_pending_delivery_does_not_text_subscriber() -> None:
    calls = []

    def fake_send(to: str, text: str, request_id: str) -> dict:
        calls.append((to, text, request_id))
        return {"message_id": "m-1"}

    result = notify_delivery(
        Delivery("asset-1", "+15550001111", "https://x.test/a", delivered=False),
        fake_send,
    )

    assert result == {"status": "pending", "asset_id": "asset-1"}
    assert calls == []


def test_delivered_asset_sends_one_stable_alert() -> None:
    calls = []

    def fake_send(to: str, text: str, request_id: str) -> dict:
        calls.append((to, text, request_id))
        return {"message_id": "m-2"}

    result = notify_delivery(
        Delivery("asset-2", "+15550002222", "https://x.test/b", delivered=True),
        fake_send,
    )

    assert result == {"message_id": "m-2"}
    assert calls == [("+15550002222", "Your creator download is ready: https://x.test/b", "asset-asset-2")]
