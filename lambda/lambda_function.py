
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def lambda_handler(event, context):
    product = event.get("product")

    if not isinstance(product, dict):
        raise ValueError("Product must be a JSON object")

    product_id = product.get("id")
    name = product.get("name")
    quantity = product.get("quantity")
    discount_percent = product.get("discountPercent", 0)
    price_value = product.get("unitPrice")

    if not isinstance(product_id, str) or not product_id.strip():
        raise ValueError("Product ID is required")

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Product name is required")

    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be a positive integer")

    if type(discount_percent) is not int or not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")

    if not isinstance(price_value, str):
        raise ValueError("Unit price must be a decimal string")

    try:
        unit_price = Decimal(price_value)
    except InvalidOperation as exc:
        raise ValueError("Invalid unit price") from exc

    if (
        not unit_price.is_finite()
        or unit_price <= 0
        or unit_price.as_tuple().exponent < -2
    ):
        raise ValueError("Unit price must be positive with at most 2 decimal places")

    subtotal = unit_price * quantity

    discount = (
        subtotal * Decimal(discount_percent) / Decimal("100")
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    total = subtotal - discount

    return {
        "status": "PROCESSED",
        "productId": product_id,
        "currency": "GBP",
        "subtotal": f"{subtotal:.2f}",
        "discount": f"{discount:.2f}",
        "total": f"{total:.2f}"
    }
