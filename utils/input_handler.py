import json
from pathlib import Path
import pandas as pd


def manual_input():
    print("\n--- Manual Invoice Input ---")

    company_name = input("Company Name: ")
    company_address = input("Company Address: ")

    customer_name = input("Customer Name: ")
    customer_email = input("Customer Email: ")

    items = []

    while True:
        name = input("\nItem Name: ")
        qty = int(input("Quantity: "))
        price = float(input("Price: "))

        items.append({
            "name": name,
            "quantity": qty,
            "price": price
        })

        more = input("Add another item? (y/n): ")

        if more.lower() != "y":
            break

    tax_rate = float(input("Tax Rate (example 0.18): "))
    discount = float(input("Discount: "))

    return {
        "company": {"name": company_name, "address": company_address},
        "customer": {"name": customer_name, "email": customer_email},
        "items": items,
        "tax_rate": tax_rate,
        "discount": discount
    }


def json_input(path):
    p = Path(path)
    with p.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def excel_input(path):
    df = pd.read_excel(path)

    items = []

    for _, row in df.iterrows():
        items.append({
            "name": row["Item"],
            "quantity": int(row["Quantity"]),
            "price": float(row["Price"])
        })

    return {
        "company": {
            "name": "Excel Imported Company",
            "address": "Auto Generated"
        },
        "customer": {
            "name": "Excel Client",
            "email": "excel@client.com"
        },
        "items": items,
        "tax_rate": 0.18,
        "discount": 0
    }
