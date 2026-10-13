"""Domain model for a creator's digital-asset delivery notification."""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Delivery:
    asset_id: str
    subscriber_phone: str
    download_url: str
    delivered: bool = False


def notify_delivery(
    delivery: Delivery,
    send: Callable[[str, str, str], dict],
) -> dict:
    """Notify only after delivery is recorded, keeping the state transition explicit."""
    if not delivery.delivered:
        return {"status": "pending", "asset_id": delivery.asset_id}
    message = f"Your creator download is ready: {delivery.download_url}"
    return send(delivery.subscriber_phone, message, f"asset-{delivery.asset_id}")
