import re
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# ==========================================
# EMBEDDING MODEL
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================
# LOAD SCHEMA FILE
# ==========================================

with open("DataBase/sangam_schema.txt", "r", encoding="utf-8") as file:
    schema_text = file.read()

# ==========================================
# SPLIT TABLES
# ==========================================

# Split schema using "Table:"
tables = re.split(r"(?=Table:)", schema_text)

documents = []

# ==========================================
# CREATE TABLE-WISE DOCUMENTS
# ==========================================

for table in tables:

    table = table.strip()

    if not table:
        continue

    # Extract table name
    match = re.search(r"Table:\s*(\w+)", table)

    if match:
        table_name = match.group(1)

    else:
        table_name = "unknown"

    # ======================================
    # CREATE DOCUMENT
    # ======================================

    doc = Document(
        page_content=table,
        metadata={
            "table_name": table_name
        }
    )

    documents.append(doc)

# ==========================================
# STORE IN CHROMADB
# ==========================================

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print(f"\nStored {len(documents)} table embeddings successfully.")