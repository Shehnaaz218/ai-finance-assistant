from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

def rag_query(query):
    try:
        # Check if file exists
        if not os.path.exists("data/finance.txt"):
            return "Error: finance.txt not found"

        # Load documents
        loader = TextLoader("data/finance.txt")
        documents = loader.load()

        # Split text
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)

        # Embeddings
        embedding = OpenAIEmbeddings()

        # Vector DB
        db = Chroma.from_documents(docs, embedding)

        # LLM
        llm = ChatOpenAI()

        results = db.similarity_search(query, k=2)
        context = " ".join([doc.page_content for doc in results])

        response = llm.invoke(f"Answer using this context: {context}\nQuestion: {query}")
        return response.content

    except Exception as e:
        return f"RAG Error: {str(e)}"