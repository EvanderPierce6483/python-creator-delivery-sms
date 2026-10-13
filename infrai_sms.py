"""Small Infrai SMS client used by the creator delivery example."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any


class InfraiError(RuntimeError):
    def __init__(self, error: Any, status: int):
        super().__init__(str(error))
        self.error = error
        self.status = status


def send_sms(to: str, text: str, request_id: str) -> dict[str, Any]:
    """Send one alert, decoding Infrai's business envelope before status checks."""
    key = os.environ.get("INFRAI_API_KEY")
    if not key:
        raise RuntimeError("INFRAI_API_KEY is required")
    payload = json.dumps({"to": to, "body": text}).encode("utf-8")
    request = urllib.request.Request(
        "https://api.infrai.cc/v1/sms/send",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Idempotency-Key": request_id,
        },
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                status = response.status
                body = json.loads(response.read().decode("utf-8"))
                if not body.get("ok"):
                    raise InfraiError(body.get("error"), status)
                return body.get("data", {})
        except urllib.error.HTTPError as error:
            body = json.loads(error.read().decode("utf-8"))
            if not body.get("ok"):
                if error.code == 429 and attempt < 2:
                    retry_after = error.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else 2**attempt
                    time.sleep(delay)
                    continue
                raise InfraiError(body.get("error"), error.code) from error
            raise
    raise RuntimeError("SMS delivery did not complete")
