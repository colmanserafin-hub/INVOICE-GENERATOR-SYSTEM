import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta

from utils.validator import validate_invoice_data
from utils.calculator import calculate_invoice
from utils.pdf_generator import generate_pdf
from utils.logger import log_invoice_event


def run_smoke():
    base = Path(__file__).resolve().parent
    sample_json = base / "samples" / "sample_invoice.json"

    print(f"Loading sample JSON: {sample_json}")
    with open(sample_json, "r", encoding="utf-8") as f:
        data = json.load(f)

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

    html_out = base / "invoices" / "invoice_smoke.html"
    html_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.write_text(html_content, encoding="utf-8")

    print(f"Rendered HTML saved to: {html_out}")

    pdf_out = base / "invoices" / "invoice_smoke.pdf"
    try:
        # Provide structured data as fallback for ReportLab
        data_for_pdf = {
            "company": data.get("company", {}),
            "customer": data.get("customer", {}),
            "items": data.get("items", []),
            "summary": summary,
            "invoice_no": "INV-001",
            "invoice_date": datetime.now().strftime("%B %d, %Y"),
            "due_date": (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y"),
        }
        generate_pdf(html_content, str(pdf_out), data_for_reportlab=data_for_pdf)
        print(f"PDF saved to: {pdf_out}")
    except Exception as e:
        print(f"PDF generation failed: {e}")

    log_invoice_event(str(pdf_out), summary["total"])
    print("Smoke test finished.")


if __name__ == "__main__":
    run_smoke()
