from flask import Flask, request, send_file
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import json

app = Flask(__name__)

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        request_data = request.get_json(force=True)  # Force parsing even without correct header
        json_str = json.dumps(request_data, indent=2)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("📄 Full JSON Payload Report", styles["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<pre>{json_str}</pre>", styles["Code"]))

        doc.build(elements)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="full_payload_report.pdf"
        )

    except Exception as e:
        print("❌ PDF generation failed:", str(e))
        return {"error": "PDF generation failed", "details": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7071)
