from extract_sql import extract_sql
from GeminiModel import model
import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
import mysql.connector
import re
from langchain_chroma import Chroma


db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor(dictionary=True)


# LOAD VECTOR DATABASE
# ==========================================
BLOCKED_KEYWORDS = [
    "delete",
    "drop",
    "truncate",
    "alter",
    "insert",
    "update"
]

def ask_crm(question):
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
    vectordb = Chroma(
    persist_directory="RealsangamCRMdb",
    embedding_function=embeddings
)
    retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4}
)
    # SEMANTIC RETRIEVER
    docs = retriever.invoke(question)

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])



    prompt = f"""

You are an advanced Text-to-SQL AI assistant.

Your task is to generate accurate SQL queries from natural language questions using retrieved schema context from a RAG system.
SCHEMA CONTEXT:
{context}

The retrieved context contains:

table schemas
column names
relationships
business descriptions
semantic metadata
sample values
aliases
documentation snippets

You must use the retrieved schema context as the primary source of truth.

QUESTION:
{question}

OBJECTIVE:
Convert the user's business question into an accurate SQL query by:
1.Understanding user intent
2.Understanding business semantics
3.Matching semantic meaning to retrieved schema
4.Inferring joins and relationships
5.Generating optimized SQL

rules:
if user asks something that is not in the retrieved context, say "Sorry, I don't have enough information to answer that question."

"""


 # GENERATE SQL


    sql_query = model.invoke(prompt).content

    sql_query = extract_sql(sql_query)

    try:
       sql_lower = sql_query.lower() 
       if any(sql_lower.startswith(keyword) for keyword in BLOCKED_KEYWORDS):
        print("\nError: this type of operation is not allowed.")
       else:
        cursor.execute(sql_query)

        results = cursor.fetchall()
        final_response = f"SQL Query:\n{sql_query}\n\nResults:\n{results}"
        return final_response
       
    except Exception as e:
        print(f"\nError executing query: {e}")

    



