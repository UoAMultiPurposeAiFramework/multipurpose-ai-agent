import ast
import configparser
import os
import random
from flask import Flask, request, jsonify
from pymilvus import connections, Collection, utility, FieldSchema, CollectionSchema, DataType
import fitz
from openai import OpenAI



cfp = configparser.RawConfigParser()
cfp.read("config.ini")
milvus_uri = cfp.get("example", "uri")
token = cfp.get("example", "token")
openai_key = cfp.get("example", "openAiKey")

client = OpenAI(api_key=openai_key)


connections.connect(alias="default", uri=milvus_uri, token=token)
COLLECTION_NAME = "research_papers"
dim = 1536
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)
    print(f"Dropped existing collection: {COLLECTION_NAME}")

schema = CollectionSchema(
    fields=[
        FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True, description="Primary document ID"),
        FieldSchema(name="word_count", dtype=DataType.INT64, description="Word count of document"),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim, description="Document embeddings"),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=50000, description="Raw document text")
    ],
    description="Collection for storing research papers"
)


collection = Collection(COLLECTION_NAME, schema=schema)
print("Milvus Collection Created!")


index_params = {"metric_type": "IP", "params": {"nlist": 128}}
collection.create_index(field_name="embedding", index_params=index_params)
print("Index created successfully!")



def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()



def get_embedding(text):
    """Generates an embedding using OpenAI's API with error handling."""
    try:
        response = client.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None



@app.route("/upload", methods=["POST"])
def upload_research_paper():
    """Handles PDF upload, extracts text, generates embeddings, and stores in Milvus."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save file to uploads folder
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Extract text
    pdf_text = extract_text_from_pdf(file_path)
    if not pdf_text:
        return jsonify({"error": "Extracted text is empty. Ensure the PDF is not encrypted or blank."}), 400

    word_count = len(pdf_text.split())

    # Convert text to vector embedding
    embedding = get_embedding(pdf_text)
    if not embedding:
        return jsonify({"error": "Failed to generate embedding."}), 500

    # Generate a random document ID
    # Generate a random document ID
    doc_id = random.randint(1, 100000)

    # Insert into Milvus
    collection.insert([
        {
            "doc_id": doc_id,
            "word_count": word_count,
            "embedding": embedding,
            "text": pdf_text
        }
    ])

    return jsonify({"message": "Research paper stored successfully", "doc_id": doc_id})



@app.route("/query", methods=["POST"])
def query_research_paper():
    """Handles user queries by searching for similar text in Milvus."""
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    query_embedding = get_embedding(user_query)

    search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
    top_k = data.get("top_k", 3)

    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["doc_id", "text"]
    )

    retrieved_data = [{"doc_id": hit.get("doc_id"), "text": hit.get("text")} for hit in results[0]]

    return jsonify({"query": user_query, "results": retrieved_data})


@app.route("/ask", methods=["POST"])
def query_research_paper1():
    """Searches Milvus and sends results to OpenAI for answer generation."""
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    query_embedding = get_embedding(user_query)

    collection.load()

    search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
    top_k = data.get("top_k", 3)

    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["doc_id", "text"]
    )

    retrieved_data = []
    for hit in results[0]:
        hit_str = str(hit)  # Convert to string
        try:
            retrieved_data.append({"result": hit_str})
        except Exception as e:
            print(f"Error parsing search result: {e}")

    context = retrieved_data

    prompt = f"Use the following retrieved documents to answer the user's question:\n\n{context}\n\nUser's Question: {user_query}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI research assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return jsonify({"query": user_query, "openai_response": answer})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
