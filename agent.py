
from extract_sql import extract_sql
from GeminiModel import model
from langchain_huggingface import HuggingFaceEmbeddings
from DB_conn import get_connection
from langchain_chroma import Chroma
db = get_connection()

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

def ask_crm(question):
   
    # SEMANTIC RETRIEVER
    docs = retriever.invoke(question)

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])



    prompt = f"""

You are an expert Text-to-SQL Engine.

Your task is to convert natural language business questions into accurate MySQL queries using the provided CRM schema context.

here are some crm terms to understand
LEADS:
Potential customers who have shown interest.
Leads may come from Website, Referral, Facebook, Cold Calling, etc.
Leads can later become Opportunities.

OPPORTUNITIES:
Qualified leads with a realistic chance of becoming customers.
Represents active sales deals.
Opportunity owner is usually stored in assigned_user_id.

USERS:
CRM employees such as Sales Executives, Managers, Support Engineers, Administrators.
Users own Leads, Opportunities, Tickets, Quotations and Tasks.

TICKETS:
Customer support requests.
Used for issue tracking and resolution.

QUOTATIONS:
Commercial proposals sent to customers.
Usually generated for Opportunities.

PRODUCTS:
Products or services sold by the organization.

TASKS:
Activities performed by CRM users such as meetings, calls, visits and follow-ups


SCHEMA CONTEXT:
{context}

QUESTION:
{question}

OBJECTIVE:
1.Understand the business meaning of the question.

2.Use ONLY information present in the schema context.
3.Use ONLY tables present in the retrieved schema.
4.Use ONLY columns present in the retrieved schema.
5.Never assume columns exist.
6.Never assume tables exist.
7.Never create imaginary relationships.
8.Generate joins ONLY if:
    relationship information exists in schema context
    OR
    foreign key meaning is explicitly obvious from retrieved context.
9.If data exists in a single table:
DO NOT generate joins.
10.Optimize query readability.
11.Generate valid MySQL syntax only.

STRICT SCHEMA GROUNDING RULES

Never use a column unless it appears in the retrieved schema.

Before generating SQL:

1. Identify all required tables.
2. Verify every column exists in those tables.
3. Verify every JOIN column exists in both tables.

If a column is not present in the schema context:
DO NOT USE IT.

Never assume foreign keys.

Never invent relationships.

Never invent columns.


note:
If no exact match exists:
Search for semantically equivalent columns.
Search for business synonyms.
Search for CRM terminology mappings.

Examples:

User says: "manager"
Schema contains: user_type
Meaning:
manager is a value stored inside users.user_type

User says: "designation"
Schema contains: user_type
Meaning:
designation is represented by user_type

User says: "employee"
Schema contains: users table
Meaning:
employee = CRM user

User says: "deal"
Schema contains: opportunities table
Meaning:
deal = opportunity

User says: "customer"
Schema contains: leads table
Meaning:
customer/prospect = lead

User says: "owner"
Schema contains: assigned_user_id
Meaning:
owner = assigned user

Never create non-existing tables.

BAD:
SELECT * FROM designations;

when designations table does not exist.
2.If the answer cannot be generated using the retrieved schema context:
Return ONLY:
NO_SQL_POSSIBLE
"""


 # GENERATE SQL


    sql_query = model.invoke(prompt).content

    sql_query = extract_sql(sql_query)
    print(sql_query)

    try:
       sql_lower = sql_query.lower() 
       print(sql_query)
       if any(sql_lower.startswith(keyword) for keyword in BLOCKED_KEYWORDS):
        print("\nError: this type of operation is not allowed.")
       else:
        print(sql_query)
        cursor.execute(sql_query)

        results = cursor.fetchall()
        final_response = f"SQL Query:\n{sql_query}\n\nResults:\n{results}"
        print(final_response)
        return final_response
       
    except Exception as e:
        value=(f"\nError executing query: {e}")
        return value

    



