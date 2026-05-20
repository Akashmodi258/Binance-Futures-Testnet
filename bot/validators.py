VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s:
        raise ValidationError("Symbol cannot be empty.")
    if not s.isalnum():
        raise ValidationError(f"Invalid symbol '{s}'. Use alphanumeric only (e.g. BTCUSDT).")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{s}'. Must be one of: {', '.join(VALID_SIDES)}.")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{t}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}."
        )
    return t


def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid quantity '{quantity}'. Must be a positive number.")
    if q <= 0:
        raise ValidationError("Quantity must be greater than zero.")
    return q


def validate_price(price: str) -> float:
    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid price '{price}'. Must be a positive number.")
    if p <= 0:
        raise ValidationError("Price must be greater than zero.")
    return p


def validate_inputs(symbol, side, order_type, quantity, price=None):
    """
    Validate all inputs and return cleaned values.
    Returns (symbol, side, order_type, quantity, price).
    price is None for MARKET orders.
    """
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)

    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        price = validate_price(price)
    else:
        price = None

    return symbol, side, order_type, quantity, price
