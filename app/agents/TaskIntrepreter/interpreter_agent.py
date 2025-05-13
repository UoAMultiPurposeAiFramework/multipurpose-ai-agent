from flask import Flask, request, send_file
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/interpret", methods=["POST"])
def interpret():
    user_prompt = request.json.get("prompt")

    # Hardcoded interpretation for now
    agent1_resp = requests.post("http://multi-purpose-ai-sqlliteagent:7070/query", json={
        "user_prompt":user_prompt ,
        "database_name": "finance_db"
    })

    result = agent1_resp.json()
    if "results" not in result:
        return result, 400

    pdf_resp = requests.post("http://multi-purpose-ai-pdfagent:7071/generate-pdf", json={
        "results": result["results"],
        "sql_query": result["sql_query"],
        "user_prompt": result["user_prompt"]
    })

    return send_file(BytesIO(pdf_resp.content), mimetype="application/pdf", as_attachment=True, download_name="report.pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7073)
