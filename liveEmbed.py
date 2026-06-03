import os
from dotenv import load_dotenv
from DB_conn import get_connection
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


# ==========================================
# MYSQL CONNECTION
# ==========================================
db = get_connection()

cursor = db.cursor()


# ==========================================
# GET ALL TABLES
# ==========================================

cursor.execute("SHOW TABLES")

tables = cursor.fetchall()

documents = []


# ==========================================
# TABLE → SINGLE CHUNK
# ==========================================

for table in tables:

    table_name = table[0]

    print(f"Processing Table: {table_name}")

    cursor.execute(f"DESCRIBE {table_name}")

    columns = cursor.fetchall()


    # ======================================
    # BUILD TABLE CONTEXT
    # # ======================================

    table_context = f"Table Name: {table_name}\nColumns:"

    for column in columns:

        col_name = column[0]
        col_type = column[1]

        table_context += f"\n- {col_name} ({col_type})"

    # print(table_context)
    # ======================================
    # ADD SAMPLE ROWS
    # ======================================

    # try:

    #     cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")

    #     rows = cursor.fetchall()

    #     table_context += "\n\nSAMPLE DATA:\n"

    #     for row in rows:

    #         table_context += f"\n{row}"

    # except:
    #     pass


    # ======================================
    # CREATE DOCUMENT
    # ======================================

    doc = Document(
        page_content=table_context,
        metadata={
            "table_name": table_name
            
        }
    )

    documents.append(doc)

# print(documents)

# ==========================================
# EMBEDDING MODEL
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================
# ==========================================
# STORE IN CHROMADB
# ==========================================

vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="RealsangamCRMdb",
)



print("\nAll Tables Embedded Successfully")