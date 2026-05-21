from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings()
retriever = FAISS.from_texts([], embeddings).as_retriever()





@tool
def retrieve_schema(question: str) -> str:
    """
    Retrieves relevant schema context
    based on user question.
    """

    docs = retriever.invoke(question)

    schema_context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return schema_context

tools = [retrieve_schema]