def validate_invoice_data(data):
    required = ["company", "customer", "items"]

    for field in required:
        if field not in data:
            raise ValueError(f"Missing field: {field}")

    if not isinstance(data["items"], list) or len(data["items"]) == 0:
        raise ValueError("Item list cannot be empty")

    for item in data["items"]:
        if "quantity" not in item or "price" not in item or "name" not in item:
            raise ValueError("Each item must contain 'name', 'quantity' and 'price'")

        if item["quantity"] <= 0:
            raise ValueError("Quantity must be positive")

        if item["price"] < 0:
            raise ValueError("Price cannot be negative")

    return True
