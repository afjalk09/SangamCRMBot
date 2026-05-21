from dotenv import load_dotenv
load_dotenv()

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# ==========================================
# EMBEDDINGS
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================
# LOAD CHROMADB
# ==========================================

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# ==========================================
# RETRIEVER
# ==========================================

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

# ==========================================
# GEMINI MODEL
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5
)

# ==========================================
# SQL PROMPT
# ==========================================

SQL_PROMPT = """
You are an expert MySQL engineer.

Generate accurate MySQL query.

RULES:
1. Use ONLY provided schema
2. Never hallucinate tables
3. Never hallucinate columns
4. Never use DELETE, DROP, UPDATE, ALTER
5. Return ONLY SQL query
6. Use proper JOINs
7. Use MySQL syntax only
8. Use LIMIT 100 unless specified

=================================
SCHEMA CONTEXT
=================================

{schema_context}

=================================
USER QUESTION
=================================

{question}

=================================
OUTPUT
=================================

Return ONLY SQL query.
"""

prompt = PromptTemplate(
    template=SQL_PROMPT,
    input_variables=["schema_context", "question"]
)

# ==========================================
# RETRIEVE SCHEMA
# ==========================================

def retrieve_schema(user_question):

    docs = retriever.invoke(user_question)

    schema_context = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    return schema_context

# ==========================================
# GENERATE SQL
# ==========================================

def generate_sql(user_question):

    # STEP 1 → Retrieve Schema
    schema_context = retrieve_schema(user_question)

    print("\n======================")
    print("RETRIEVED SCHEMA")
    print("======================\n")

    print(schema_context)

    # STEP 2 → Create Chain
    chain = prompt | llm

    # STEP 3 → Generate SQL
    response = chain.invoke({
        "schema_context": schema_context,
        "question": user_question
    })

    sql_query = response.content.strip()

    # Remove markdown
    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")

    return sql_query



question = "show me recents name of leads and their assigned salespersons"
sql_query = generate_sql(question)
print("\n======================")

print("GENERATED SQL QUERY")
print("======================\n")
print(sql_query)