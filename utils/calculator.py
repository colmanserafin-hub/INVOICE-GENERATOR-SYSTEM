def calculate_invoice(items, tax_rate, discount):
    subtotal = 0

    for item in items:
        subtotal += item["quantity"] * item["price"]

    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount - discount

    return {
        "subtotal": round(subtotal, 2),
        "tax": round(tax_amount, 2),
        "discount": round(discount, 2),
        "total": round(total, 2)
    }
