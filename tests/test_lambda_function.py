
import pytest

from lambda_function import lambda_handler


def test_process_valid_product():
    event = {
        "product": {
            "id": "PROD-001",
            "name": "Mechanical Keyboard",
            "unitPrice": "49.90",
            "quantity": 2,
            "discountPercent": 10,
        }
    }

    result = lambda_handler(event, None)

    assert result == {
        "status": "PROCESSED",
        "productId": "PROD-001",
        "currency": "GBP",
        "subtotal": "99.80",
        "discount": "9.98",
        "total": "89.82",
    }


def test_process_product_without_discount():
    event = {
        "product": {
            "id": "PROD-002",
            "name": "Mouse",
            "unitPrice": "25.00",
            "quantity": 3,
        }
    }

    result = lambda_handler(event, None)

    assert result["subtotal"] == "75.00"
    assert result["discount"] == "0.00"
    assert result["total"] == "75.00"


def test_discount_rounding():
    event = {
        "product": {
            "id": "PROD-003",
            "name": "Small Item",
            "unitPrice": "0.05",
            "quantity": 3,
            "discountPercent": 10,
        }
    }

    result = lambda_handler(event, None)

    assert result["discount"] == "0.02"
    assert result["total"] == "0.13"


@pytest.mark.parametrize(
    "field,value,error_message",
    [
        ("quantity", 0, "Quantity must be a positive integer"),
        ("quantity", -2, "Quantity must be a positive integer"),
        ("unitPrice", "-10.00", "Unit price must be positive"),
        ("unitPrice", "invalid", "Invalid unit price"),
        ("discountPercent", 110, "Discount must be between"),
    ],
)
def test_reject_invalid_product(field, value, error_message):
    product = {
        "id": "PROD-004",
        "name": "Keyboard",
        "unitPrice": "49.90",
        "quantity": 2,
    }

    product[field] = value

    with pytest.raises(ValueError, match=error_message):
        lambda_handler({"product": product}, None)
