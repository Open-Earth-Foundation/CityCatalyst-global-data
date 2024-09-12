from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()


def load_vectorstore():
    print("\nLoading vector store\n")
    # Create embeddings model
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
    )

    # Create Chroma vector store
    vector_store = Chroma(
        collection_name="GPC_Full_MASTER_RW_v7",
        embedding_function=embeddings,
        persist_directory="../chroma_langchain_db",
    )

    return vector_store
