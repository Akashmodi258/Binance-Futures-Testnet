import hashlib
import hmac
import time
import urllib.parse

import requests

from bot.logging_config import setup_logging

BASE_URL = "https://testnet.binancefuture.com"
logger = setup_logging().getChild("client")


class BinanceAPIError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"Binance API error {code}: {message}")


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _post(self, endpoint: str, params: dict) -> dict:
        params = self._sign(params)
        url = BASE_URL + endpoint
        logger.debug("POST %s | params: %s", url, {k: v for k, v in params.items() if k != "signature"})
        try:
            resp = self.session.post(url, params=params, timeout=10)
        except requests.exceptions.ConnectionError as e:
            logger.error("Network error: %s", e)
            raise ConnectionError(f"Network error: {e}") from e
        except requests.exceptions.Timeout:
            logger.error("Request timed out for %s", url)
            raise TimeoutError("Request timed out. Check your connection.")

        logger.debug("Response HTTP %s: %s", resp.status_code, resp.text)
        print(f"[DEBUG] HTTP {resp.status_code}: {resp.text}")

        if not resp.text:
            raise Exception(f"Empty response from server (HTTP {resp.status_code})")

        data = resp.json()
        if "code" in data and data["code"] != 200:
            raise BinanceAPIError(data["code"], data.get("msg", "Unknown error"))

        return data

    def place_order(self, symbol, side, order_type, quantity, price=None):
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"
        return self._post("/fapi/v1/order", params)