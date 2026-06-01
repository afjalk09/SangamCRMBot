import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
import mysql.connector

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_chroma import Chroma

from GeminiModel import model

from rich import print



import re


load_dotenv()


# ==========================================
# MYSQL CONNECTION
# ==========================================

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor(dictionary=True)


# ==========================================
# LOAD VECTOR DATABASE
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vectordb = Chroma(
    persist_directory="RealsangamCRMdb",
    embedding_function=embeddings
)


# ==========================================
# SEMANTIC RETRIEVER
# ==========================================

retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4}
)






def extract_sql(text):

    # Remove markdown
    text = text.replace("```sql", "")
    text = text.replace("```", "")

    # Match WITH ... ; OR SELECT ... ;
    match = re.search(
        r"((WITH[\s\S]*?;)|(SELECT[\s\S]*?;))",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return text.strip()


# ==========================================
# QUESTION LOOP
# ==========================================

while True:

    question = input("\nAsk CRM Question: ")


    # ======================================
    # SEMANTIC SEARCH
    # ======================================

    docs = retriever.invoke(question)

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])


    # print("\nRetrieved Context:\n")

    # print(context)


    # ======================================
    # SQL GENERATION PROMPT
    # ======================================

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


    # ======================================
    # GENERATE SQL
    # ======================================

    sql_query = model.invoke(prompt).content

    sql_query = extract_sql(sql_query)

    print("\nGenerated SQL:\n")

    print(sql_query)





    
    # ======================================
    # EXECUTE SQL
    # ======================================

    BLOCKED_KEYWORDS = [
    "delete",
    "drop",
    "truncate",
    "alter",
    "insert",
    "update"
]


    try:
       sql_lower = sql_query.lower() 
       if any(keyword in sql_lower for keyword in BLOCKED_KEYWORDS):
            print("\nError: this type of operation is not allowed.")
       else:
        cursor.execute(sql_query)

        results = cursor.fetchall()

        print("\nResults:\n")

        for row in results:

            print(row)

        # ======================================
    #     # BUSINESS ANALYSIS PROMPT
    #     analysis_prompt = f"""

    # You are a senior CRM business consultant.

    # User Question:
    # {question}

    # Database Results:
    # {results}

    # Analyze the business patterns and provide:
    # 1. Key insights
    # 2. Profit improvement recommendations
    # 3. Customer strategy
    # 4. Lead source recommendations

    # """
        # analysis = model.invoke(analysis_prompt).content.strip()

        # print("\nBusiness Analysis:\n")
        # print(analysis)
    except Exception as e:
        print(f"\nError executing query: {e}")

    
   