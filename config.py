"""
Company branding and payment configuration for invoices.
Customize these values with your company details and logo.

LOGO_URL can be:
1. Local file path: "C:/path/to/logo.jpg" or "./logo.png" 
2. Online URL: "https://example.com/logo.jpg"
3. Base64 data URL: "data:image/jpeg;base64,..."

Example: "C:/Users/YourName/Pictures/serafin_logo.jpg"
"""

# Company branding
COMPANY = {
    "name": "Your Company Name",
    "address": "123 Business Street, Suite 100",
    "city_state_zip": "New York, NY 10001",
    "phone": "+1 (555) 123-4567",
    "email": "info@yourcompany.com",
    "website": "www.yourcompany.com",
    "logo_url": r"C:\Users\HP\Downloads\LOGO.jpeg",  # Use raw string r"..." or forward slashes: C:/Users/HP/Downloads/LOGO.jpeg
}

# Payment details for footer
PAYMENT_INFO = {
    "bank_name": "Your Bank Name",
    "account_holder": "Your Company Name",
    "account_number": "****1234",
    "routing_number": "****5678",
    "swift_code": "SWIFTCODE",
    "methods": "Bank Transfer, Credit Card, Check",
}

# Invoice settings
INVOICE_SETTINGS = {
    "default_due_days": 30,  # Payment terms: Net 30
    "currency": "USD",
    "tax_label": "Sales Tax",
}

# Footer message and terms
FOOTER_MESSAGE = "Thank you for your business!"
TERMS_AND_CONDITIONS = "Payment is due within 30 days. Late payments may incur interest charges."

# Color scheme (hex colors)
COLORS = {
    "primary": "#1f3c88",       # Dark blue
    "secondary": "#2e86de",     # Light blue
    "accent": "#ffb703",         # Amber/gold
    "header_bg": "#f8f9fa",      # Light gray background for better contrast
    "header_accent": "#1f3c88",  # Dark blue accent stripe
    "header_text": "#1a1a1a",    # Dark text for visibility
    "header_text_light": "#666666",  # Light gray for secondary text
    "table_header_bg": "#f4f6f9",
    "table_alt_row": "#f9fafb",
    "text_dark": "#1a1a1a",
    "text_light": "#666666",
    "border_color": "#ddd",
}
