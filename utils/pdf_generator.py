from pathlib import Path
from datetime import datetime, timedelta


def _pdf_with_weasy(html_content, out_path):
    from weasyprint import HTML
    HTML(string=html_content).write_pdf(str(out_path))


def _pdf_with_reportlab(data, out_path):
    # Professional invoice renderer using ReportLab
    import sys
    from pathlib import Path as PathlibPath
    
    # Add parent to path to import config
    sys.path.insert(0, str(PathlibPath(__file__).resolve().parent.parent))
    from config import COMPANY, PAYMENT_INFO, INVOICE_SETTINGS, FOOTER_MESSAGE, COLORS
    
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.units import mm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.pdfgen import canvas

    # Custom page template for footer at bottom
    class FooterPageTemplate:
        def __init__(self, story, footer_text, colors_dict):
            self.story = story
            self.footer_text = footer_text
            self.colors_dict = colors_dict
        
        def on_page(self, canvas, doc):
            canvas.saveState()
            # Footer at bottom of page
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(rl_colors.HexColor(self.colors_dict.get('text_light', '#666')))
            canvas.drawCentredString(105*mm, 10*mm, self.footer_text)
            canvas.drawString(15*mm, 5*mm, f"Invoice Generated: {INVOICE_SETTINGS.get('default_due_days', 30)} day payment terms")
            canvas.restoreState()

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=25 * mm,
    )
    
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=rl_colors.HexColor(COLORS['primary']),
        spaceAfter=6,
        fontName='Helvetica-Bold',
    )
    
    company_style = ParagraphStyle(
        'CompanyName',
        parent=styles['Normal'],
        fontSize=16,
        textColor=rl_colors.HexColor(COLORS['text_dark']),
        fontName='Helvetica-Bold',
        spaceAfter=3,
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=rl_colors.HexColor(COLORS['text_light']),
        fontName='Helvetica-Bold',
    )

    company = data.get("company", {})
    customer = data.get("customer", {})
    items = data.get("items", [])
    summary = data.get("summary", {})
    invoice_no = data.get("invoice_no", "INV-001")
    invoice_date = data.get("invoice_date", datetime.now().strftime("%B %d, %Y"))
    due_date = data.get("due_date", (datetime.now() + timedelta(days=INVOICE_SETTINGS['default_due_days'])).strftime("%B %d, %Y"))

    # --- HEADER SECTION ---
    header_data = [[
        Paragraph(f"<b>{COMPANY['name']}</b><br/><font size=8>{COMPANY['address']}<br/>{COMPANY['city_state_zip']}</font>", label_style),
        Paragraph(f"<b>INVOICE</b>", title_style)
    ]]
    
    header_table = Table(header_data, colWidths=[100 * mm, 68 * mm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), rl_colors.HexColor(COLORS['header_bg'])),
        ('TEXTCOLOR', (0, 0), (-1, -1), rl_colors.HexColor(COLORS['header_text'])),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (0, 0), 12),
        ('RIGHTPADDING', (1, 0), (1, 0), 12),
        ('INNERGRID', (0, 0), (-1, -1), 0, rl_colors.white),
        ('BOX', (0, 0), (-1, -1), 2, rl_colors.HexColor(COLORS['header_accent'])),
        ('ROWHEIGHTS', (0, 0), (-1, -1), 50),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 6))

    # --- INVOICE META DATA (Left: Bill To, Right: Invoice Details) ---
    meta_data = [[
        Paragraph(f"<b>Bill To:</b><br/><font size=10><b>{customer.get('name','')}</b></font><br/><font size=9>{customer.get('email','')}</font>", label_style),
        Paragraph(
            f"<b>Invoice Number:</b> {invoice_no}<br/>"
            f"<b>Invoice Date:</b> {invoice_date}<br/>"
            f"<b>Due Date:</b> {due_date}",
            label_style
        )
    ]]
    
    meta_table = Table(meta_data, colWidths=[100 * mm, 68 * mm])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 0.25, rl_colors.HexColor(COLORS['border_color'])),
        ('ROWHEIGHTS', (0, 0), (-1, -1), 30),
    ]))
    
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # --- LINE ITEMS TABLE ---
    table_data = [["Description", "Quantity", "Unit Price", "Total"]]
    
    for idx, it in enumerate(items):
        name = it.get("name", "")
        qty = it.get("quantity", 0)
        price = it.get("price", 0.0)
        total = qty * price
        
        table_data.append([
            Paragraph(name, styles['Normal']),
            Paragraph(str(qty), styles['Normal']),
            Paragraph(f"{price:,.2f}", styles['Normal']),
            Paragraph(f"{total:,.2f}", styles['Normal']),
        ])

    col_widths = [80 * mm, 22 * mm, 33 * mm, 33 * mm]
    items_table = Table(table_data, colWidths=col_widths)
    
    # Alternating row colors
    style_list = [
        ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor(COLORS['table_header_bg'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.HexColor(COLORS['text_dark'])),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.25, rl_colors.HexColor(COLORS['border_color'])),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWHEIGHTS', (0, 0), (-1, -1), 18),
    ]
    
    # Add alternating row colors
    for row_idx in range(1, len(table_data)):
        if row_idx % 2 == 0:
            style_list.append(('BACKGROUND', (0, row_idx), (-1, row_idx), rl_colors.HexColor(COLORS['table_alt_row'])))
    
    items_table.setStyle(TableStyle(style_list))
    story.append(items_table)
    story.append(Spacer(1, 12))

    # --- TOTALS SECTION ---
    totals_data = [
        ["Subtotal:", Paragraph(f"{summary.get('subtotal', 0):,.2f}", styles['Normal'])],
        ["Tax:", Paragraph(f"{summary.get('tax', 0):,.2f}", styles['Normal'])],
        ["Discount:", Paragraph(f"-{summary.get('discount', 0):,.2f}", styles['Normal'])],
        ["Total Due:", Paragraph(f"<b>{summary.get('total', 0):,.2f}</b>", styles['Normal'])],
    ]
    
    totals_table = Table(totals_data, colWidths=[130 * mm, 38 * mm], hAlign='RIGHT')
    totals_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 2), rl_colors.HexColor(COLORS['table_alt_row'])),
        ('BACKGROUND', (0, 3), (-1, 3), rl_colors.HexColor(COLORS['accent'])),
        ('TEXTCOLOR', (0, 3), (0, 3), rl_colors.black),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 3), (-1, 3), 12),
        ('GRID', (0, 0), (-1, -1), 0.25, rl_colors.HexColor(COLORS['border_color'])),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWHEIGHTS', (0, 0), (-1, -1), 16),
    ]))
    
    story.append(totals_table)
    story.append(Spacer(1, 16))

    # --- PAYMENT INFO SECTION ---
    payment_text = (
        f"<b>Payment Instructions:</b><br/>"
        f"Bank: {PAYMENT_INFO['bank_name']}<br/>"
        f"Account: {PAYMENT_INFO['account_holder']}<br/>"
        f"Methods: {PAYMENT_INFO['methods']}"
    )
    story.append(Paragraph(payment_text, label_style))
    story.append(Spacer(1, 8))

    # --- FOOTER MESSAGE ---
    story.append(Paragraph(f"<i>{FOOTER_MESSAGE}</i>", ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=rl_colors.HexColor(COLORS['text_light']), alignment=TA_CENTER)))

    doc.build(story)


def generate_pdf(html_content, output_path, data_for_reportlab=None):
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Try WeasyPrint first (best HTML fidelity)
    try:
        _pdf_with_weasy(html_content, out_path)
        print("PDF Generated Successfully with WeasyPrint ✔")
        return
    except Exception:
        # Fallback to ReportLab if WeasyPrint or native libs are unavailable
        pass

    try:
        # data_for_reportlab is expected to be a dict with company/customer/items/summary
        if data_for_reportlab is None:
            raise RuntimeError("No structured data provided for ReportLab fallback")

        _pdf_with_reportlab(data_for_reportlab, out_path)
        print("PDF Generated Successfully with ReportLab (fallback) ✔")
    except Exception as e:
        raise RuntimeError(f"PDF generation failed (both methods): {e}") from e
