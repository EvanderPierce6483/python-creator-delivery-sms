"""Runnable entry point for one delivered creator asset."""

import os

from creator_alerts import Delivery, notify_delivery
from infrai_sms import send_sms


def main() -> None:
    phone = os.environ.get("DEMO_PHONE")
    if not phone:
        raise RuntimeError("DEMO_PHONE is required")
    delivery = Delivery(
        asset_id="course-lesson-07",
        subscriber_phone=phone,
        download_url="https://creator.example/download/course-lesson-07",
        delivered=True,
    )
    result = notify_delivery(delivery, send_sms)
    print("delivery alert accepted:", result)


if __name__ == "__main__":
    main()
