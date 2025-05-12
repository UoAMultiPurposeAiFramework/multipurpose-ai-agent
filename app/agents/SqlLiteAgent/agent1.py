import os, json, sqlite3
from flask import Flask, request, jsonify
from dotenv import load_dotenv

USE_MOCK = False

app = Flask(__name__)

# Setup OpenAI client for >= 1.0.0
if not USE_MOCK:
    from openai import OpenAI
    load_dotenv()
    client = OpenAI(api_key)

@app.route("/query", methods=["POST"])
def generate_and_execute_sql():
    user_input = request.json.get("user_prompt")
    db_name = request.json.get("database_name")

    # Resolve paths safely
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, "schemas", f"{db_name}.json")
    db_path = os.path.join(base_dir, "db", f"{db_name}.sqlite3")

    if not os.path.exists(schema_path) or not os.path.exists(db_path):
        return jsonify({
            "error": "Schema or DB not found",
            "details": {
                "schema_path": schema_path,
                "db_path": db_path
            }
        }), 404

    with open(schema_path) as f:
        schema = json.load(f)

    prompt = f"""
You are an SQL expert. Given the schema:
{json.dumps(schema)}

Generate a SQL query for:
\"{user_input}\"

Requirements:
- The WHERE clause should be case-insensitive (e.g., use LOWER(column) = LOWER(value) or ILIKE where applicable).
- Do not enforce case sensitivity.
- Return only the SQL query.
- Do not include any explanations or commentary.
"""

    if USE_MOCK:
        sql_query = "SELECT name, amount FROM transactions JOIN users ON transactions.user_id = users.user_id WHERE category = 'Groceries';"
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            sql_query = response.choices[0].message.content.strip()
        except Exception as e:
            print("❌ OpenAI API call failed:", str(e))
            return jsonify({
                "error": "Failed to generate SQL from OpenAI",
                "details": str(e)
            }), 500

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql_query).fetchall()
            results = [dict(row) for row in rows]
    except Exception as e:
        return jsonify({"sql_query": sql_query, "error": str(e)}), 500

    return jsonify({
        "database": db_name,
        "user_prompt": user_input,
        "sql_query": sql_query,
        "results": results
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070)

