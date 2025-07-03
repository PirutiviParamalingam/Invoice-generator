from flask import Flask, send_file, render_template_string
from weasyprint import HTML
import io
import copy

app = Flask(__name__)

@app.route("/invoice-html/<order_id>")
def generate_invoice_from_html(order_id):
    order = copy.deepcopy(mock_order)
    order["invoice_number"] = order_id

    with open("invoice_template.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    rendered_html = render_template_string(html_template, **order)

    try:
        pdf_file = HTML(string=rendered_html, base_url='.').write_pdf()
    except Exception as e:
        return f"PDF generation failed: {e}", 500

    return send_file(
        io.BytesIO(pdf_file),
        download_name=f"invoice_{order_id}.pdf",
        as_attachment=True,
        mimetype="application/pdf"
    )


mock_order = {
    "invoice_date": "July 2, 2025",
    "from_address": [
        "BITSmart Technologies Proprietary Limited",
        "Level 40, 140 William Street",
        "Melbourne VIC 3000",
        "Australia",
        "ABN: 90 628 950 676"
    ],
    "bill_to": {
        "name": "John Doe",
        "address": [
            "12 Example Street",
            "Sydney NSW 2000",
            "Australia"
        ]
    },
    "ship_to": {
        "name": "Jane Smith",
        "address": [
            "98 Delivery Lane",
            "Brisbane QLD 4000",
            "Australia"
        ]
    },
    "items": [
        {"qty": 1, "item": "USB-C Cable", "price": 15.00},
        {"qty": 2, "item": "Bluetooth Mouse", "price": 25.00},
        {"qty": 1, "item": "Mechanical Keyboard", "price": 75.00}
    ],
    "subtotal": 140.00,
    "tax": 14.00,
    "shipping": 10.00,
    "total": 164.00,
    "total_paid": 164.00,
    "note": "Order processed successfully"
}

if __name__ == "__main__":
    app.run(debug=True)
