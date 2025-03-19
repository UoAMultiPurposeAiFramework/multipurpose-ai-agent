# milvusDbAgent
 
📌 Research Paper Search API (Flask + Milvus + OpenAI)
This project allows users to upload research papers (PDFs), extract text, generate vector embeddings using OpenAI, store them in Milvus, and perform intelligent searches. Users can also ask OpenAI questions based on retrieved documents.

📖 Features
✅ Upload research papers (PDFs) and store them in Milvus
✅ Extract text from PDFs using PyMuPDF (Fitz)
✅ Generate embeddings using OpenAI's text-embedding-ada-002
✅ Perform vector-based similarity search using Milvus
✅ Use OpenAI's GPT-4o to generate answers from retrieved research papers


[example]
uri = "your-milvus-uri"
token = "your-milvus-token"
openAiKey = "your-openai-api-key"
🔗 Running the Flask App
sh
Copy
Edit
python app.py
The server will start at http://0.0.0.0:5000

🛠 API Endpoints
📌 1. Upload Research Paper
📥 Uploads a PDF, extracts text, generates embeddings, and stores it in Milvus.

🔹 Endpoint:

http
Copy
Edit
POST /upload
🔹 Request (Form-Data)

Field	Type	Description
file	file	PDF file to upload
🔹 Response:

json
Copy
Edit
{
  "message": "Research paper stored successfully",
  "doc_id": 12345
}
📌 2. Query Research Papers
🔎 Searches Milvus for similar research papers based on text queries.

🔹 Endpoint:

http
Copy
Edit
POST /query
🔹 Request (JSON)

json
Copy
Edit
{
  "query": "What is deep learning?",
  "top_k": 3
}
🔹 Response:

json
Copy
Edit
{
  "query": "What is deep learning?",
  "results": [
    {"doc_id": 12345, "text": "Deep learning is a subset of machine learning..."},
    {"doc_id": 67890, "text": "Neural networks are the core of deep learning..."}
  ]
}
📌 3. Ask OpenAI a Question
🤖 Searches Milvus and sends retrieved documents to OpenAI's GPT-4o to generate a response.

🔹 Endpoint:

http
Copy
Edit
POST /ask
🔹 Request (JSON)

json
Copy
Edit
{
  "query": "Explain convolutional neural networks."
}
🔹 Response:

json
Copy
Edit
{
  "query": "Explain convolutional neural networks.",
  "openai_response": "A convolutional neural network (CNN) is a deep learning algorithm used in image recognition..."
}
📌 Technologies Used
Flask 🚀 – Web framework for handling API requests
Milvus 🏢 – Vector database for efficient document search
OpenAI API 🤖 – Text embeddings & GPT-4o for answering queries
PyMuPDF (Fitz) 📄 – Extract text from PDFs
📌 How It Works
1️⃣ Upload a PDF → Extracts text using PyMuPDF
2️⃣ Generate embeddings → Uses OpenAI text-embedding-ada-002
3️⃣ Store in Milvus → Saves vector embeddings for fast retrieval
4️⃣ Query Milvus → Searches for similar documents using vector similarity
5️⃣ Ask OpenAI → Retrieves relevant papers and generates a response

📌 Future Enhancements
✅ Improve document chunking for large PDFs
✅ Add metadata filtering (e.g., search by research area, year)
✅ Implement FastAPI for better performance
✅ Deploy on AWS/GCP with a scalable Milvus cluster
