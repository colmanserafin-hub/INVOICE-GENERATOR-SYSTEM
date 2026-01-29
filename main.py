from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime, timedelta

from utils.input_handler import manual_input, json_input, excel_input
from utils.validator import validate_invoice_data
from utils.calculator import calculate_invoice
from utils.pdf_generator import generate_pdf
from utils.logger import log_invoice_event


def ensure_dirs(base_path: Path):
    (base_path / "invoices").mkdir(parents=True, exist_ok=True)
    (base_path / "logs").mkdir(parents=True, exist_ok=True)


def main():
    base = Path(__file__).resolve().parent
    ensure_dirs(base)

    print("\n======= Invoice Generator System =======")
    print("1. Manual Input (Q&A)")
    print("2. JSON File Input")
    print("3. Excel File Input")

    choice = input("Select Input Method (1/2/3): ")

    if choice == "1":
        invoice_data = manual_input()

    elif choice == "2":
        path = input("Enter JSON file path: ")
        invoice_data = json_input(path)

    elif choice == "3":
        path = input("Enter Excel file path: ")
        invoice_data = excel_input(path)

    else:
        print("Invalid choice")
        return

    try:
        validate_invoice_data(invoice_data)
    except Exception as e:
        print(f"Validation error: {e}")
        return

    summary = calculate_invoice(
        invoice_data["items"],
        invoice_data.get("tax_rate", 0),
        invoice_data.get("discount", 0)
    )

    env = Environment(loader=FileSystemLoader(str(base / "templates")))
    template = env.get_template("invoice.html")

    html_content = template.render(
        company=invoice_data["company"],
        customer=invoice_data["customer"],
        items=invoice_data["items"],
        summary=summary
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = base / "invoices" / f"invoice_{timestamp}.pdf"

    data_for_pdf = {
        "company": invoice_data.get("company", {}),
        "customer": invoice_data.get("customer", {}),
        "items": invoice_data.get("items", []),
        "summary": summary,
        "invoice_no": invoice_data.get("invoice_no", f"INV-{int(datetime.now().timestamp()) % 100000:05d}"),
        "invoice_date": invoice_data.get("invoice_date", datetime.now().strftime("%B %d, %Y")),
        "due_date": invoice_data.get("due_date", (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")),
    }

    generate_pdf(html_content, str(output_file), data_for_reportlab=data_for_pdf)

    log_invoice_event(str(output_file), summary["total"])

    print("\nInvoice Generated Successfully ✅")


if __name__ == "__main__":
    main()
