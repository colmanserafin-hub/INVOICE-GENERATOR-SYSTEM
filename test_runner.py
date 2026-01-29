from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader

from utils.input_handler import json_input
from utils.validator import validate_invoice_data
from utils.calculator import calculate_invoice
from utils.pdf_generator import generate_pdf
from utils.logger import log_invoice_event


def run_test():
    base = Path(__file__).resolve().parent
    sample_json = base / "samples" / "sample_invoice.json"

    print(f"Loading sample JSON: {sample_json}")
    data = json_input(str(sample_json))

    # create a sample Excel too (for user's later testing)
    try:
        import pandas as pd
        df = pd.DataFrame([
            {"Item": "Widget A", "Quantity": 2, "Price": 49.99},
            {"Item": "Service B", "Quantity": 1, "Price": 150.0}
        ])
        excel_path = base / "samples" / "sample_invoice.xlsx"
        excel_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(str(excel_path), index=False)
        print(f"Wrote sample Excel: {excel_path}")
    except Exception as e:
        print(f"Could not write sample Excel: {e}")
        excel_path = None

    try:
        validate_invoice_data(data)
    except Exception as e:
        print(f"Validation failed: {e}")
        return

    summary = calculate_invoice(data["items"], data.get("tax_rate", 0), data.get("discount", 0))

    env = Environment(loader=FileSystemLoader(str(base / "templates")))
    template = env.get_template("invoice.html")

    html_content = template.render(
        company=data["company"],
        customer=data["customer"],
        items=data["items"],
        summary=summary
    )

    html_out = base / "invoices" / "invoice_test.html"
    html_out.parent.mkdir(parents=True, exist_ok=True)
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Rendered HTML saved to: {html_out}")

    pdf_out = base / "invoices" / "invoice_test.pdf"
    try:
        generate_pdf(html_content, str(pdf_out))
        print(f"PDF saved to: {pdf_out}")
    except Exception as e:
        print(f"PDF generation failed (this may need system libs): {e}")

    log_invoice_event(str(pdf_out), summary["total"])
    print("Smoke test finished.")

if __name__ == "__main__":
    run_test()
