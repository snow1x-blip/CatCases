from fastapi import HTTPException, Request
import hashlib
import hmac
import json
import os
import time
from urllib.parse import parse_qsl


TELEGRAM_BOT_TOKEN = "8223396167:AAFl9iMFxFcdvaLjuqWVMeuPjFwGnLHls1U"


def validate_telegram_init_data(init_data: str):
    if not TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=500, detail="TELEGRAM_BOT_TOKEN is not configured")
    if not init_data:
        raise HTTPException(status_code=401, detail="Missing Telegram init_data")

    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = pairs.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=401, detail="Invalid Telegram init_data: missing hash")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))
    secret_key = hmac.new(b"WebAppData", TELEGRAM_BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise HTTPException(status_code=401, detail="Invalid Telegram signature")

    auth_date = pairs.get("auth_date")
    if not auth_date:
        raise HTTPException(status_code=401, detail="Invalid Telegram init_data: missing auth_date")
    try:
        auth_date_int = int(auth_date)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Telegram init_data: bad auth_date")

    if time.time() - auth_date_int > 24 * 60 * 60:
        raise HTTPException(status_code=401, detail="Telegram init_data expired")

    user_raw = pairs.get("user")
    if not user_raw:
        raise HTTPException(status_code=401, detail="Invalid Telegram init_data: missing user")

    try:
        user = json.loads(user_raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=401, detail="Invalid Telegram init_data: malformed user")

    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid Telegram init_data: missing user id")
    username = user.get("username") or user.get("first_name") or "Anonymous"

    return int(user_id), username


def get_init_data_from_request(request: Request, init_data: str | None):
    return init_data or request.headers.get("x-telegram-init-data") or ""
