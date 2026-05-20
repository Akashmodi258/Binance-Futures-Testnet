from bot.client import BinanceClient
from bot.logging_config import setup_logging

logger = setup_logging().getChild("orders")


def place_order(client: BinanceClient, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    """
    Place an order and return the response dict.
    Logs the request and response.
    """
    log_params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }
    if price is not None:
        log_params["price"] = price

    logger.info("Placing order: %s", log_params)

    response = client.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )

    logger.info(
        "Order placed successfully — orderId=%s status=%s executedQty=%s avgPrice=%s",
        response.get("orderId"),
        response.get("status"),
        response.get("executedQty"),
        response.get("avgPrice"),
    )

    return response
