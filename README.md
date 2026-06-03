# Sangam CRM AI Agent

An intelligent AI-powered CRM assistant that converts natural language business questions into optimized SQL queries and retrieves meaningful insights from the Sangam CRM database.

---

# Overview

Sangam CRM AI Agent is an enterprise-grade Natural Language to SQL (NL2SQL) system designed for CRM analytics and automation.

The system allows non-technical users to ask questions like:

* "Highest sales made in which state?"
* "Show pending follow-ups"
* "Top performing sales executive"
* "How many open support tickets are there?"
* "Highest sales till now"

The AI agent understands CRM business semantics, retrieves relevant database schema context using vector embeddings, generates SQL queries using LLMs, validates them securely, executes them on MySQL, and returns meaningful results.

---

# Features

## AI-Powered SQL Generation

Converts natural language into SQL queries using LLMs.

## Semantic Schema Retrieval

Uses vector embeddings + ChromaDB to retrieve relevant CRM tables and business context.

## Business-Aware Understanding

Understands CRM concepts such as:

* sales
* revenue
* support tickets
* follow-ups
* customer communication
* opportunities

## Secure SQL Validation

Prevents:

* DELETE
* DROP
* UPDATE
* INSERT
* unsafe queries

## Enterprise CRM Intelligence

Supports:

*All Tables

## Hybrid Retrieval Architecture

Embeds:

* schema metadata
* business glossary
* SQL examples
* table relationships

---

# Tech Stack

| Technology             | Usage                  |
| ---------------------- | ---------------------- |
| Python                 | Backend                |
| LangChain              | AI orchestration       |
| ChromaDB               | Vector database        |
| HuggingFace Embeddings | Semantic embeddings    |
| Gemini / OpenAI LLM    | SQL generation         |
| MySQL                  | CRM database           |
| dotenv                 | Environment management |
   flask | frontend
---

# Project Architecture

```text
User Question
      ↓
Intent Understanding
      ↓
Retriever (ChromaDB)
      ↓
Relevant Schema + Business Context
      ↓
LLM SQL Generator
      ↓
SQL Validator
      ↓
MySQL Query Execution
      ↓
Formatted Results
```

---

# Folder Structure

```text
SangamCRM_Bot/
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── agent.py
├── liveEmbed.py
├── requirements.txt
├── .env   (do NOT push)
├── RealSangamCrmdb/ (do NOT push)
└── README.md
```

---

# Environment Variables

Create a `.env` file:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=sangam_crm

GOOGLE_API_KEY=your_gemini_key

```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/afjalk09/SangamCRMBot.git

cd SangamCRMBot
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Embedding CRM Schema

Run:

```bash
python liveEmbed.py
```

This will:

* extract database schema
* generate business metadata
* create semantic embeddings
* store vectors inside ChromaDB

---

# Running AI Agent

```bash
python app.py.py
```

---

# Example Questions

```text
highest sales till now

highest sales made in which state

top 5 sales executives

pending support tickets

show overdue followups

which lead source gives highest revenue

top states by opportunities

open tickets with high priority
```

---

# SQL Validation

The system validates:

* SQL syntax
* table names
* column names
* business rules
* dangerous keywords

Only safe `SELECT` queries are executed.

---

# Embedding Strategy

The retriever embeds:

## Schema Metadata

* tables
* columns
* data types

## Business Meaning

Example:

```text
sales = opportunities.amount
revenue = quotations.grand_total
```

## Query Examples

Natural language ↔ SQL mappings.

## Relationships

Example:

```text
opportunities.assigned_user_id → users.id
```

---

# Example Generated SQL

## User Question

```text
highest sales made in which state
```

## Generated SQL

```sql
SELECT
    state,
    SUM(amount) AS total_sales
FROM opportunities
WHERE deleted_at IS NULL
GROUP BY state
ORDER BY total_sales DESC
LIMIT 1;
```

---

# Security Features

* SQL injection prevention
* SELECT-only execution
* schema validation
* hallucination detection
* business rule enforcement

---

# Future Improvements

* Multi-agent architecture
* Dashboard generation
* Chart visualization
* Voice-based CRM assistant
* Autonomous report generation
* AI-powered forecasting
* Query optimization engine
* Real-time analytics

---

# Use Cases

* CRM analytics
* Sales intelligence
* Support monitoring
* Executive dashboards
* AI business assistant
* Natural language reporting

---

# Author

Afjal Khan

AI Developer | CRM AI Integration Engineer

---

# License

This project is licensed under the MIT License.
