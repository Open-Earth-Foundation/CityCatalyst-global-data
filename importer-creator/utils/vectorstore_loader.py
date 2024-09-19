import sys
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()


def load_vectorstore():
    try:
        print("\nLoading vector store\n")

        # Create embeddings model
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
        )

        # Create Chroma vector store
        vector_store = Chroma(
            collection_name="GPC_Full_MASTER_RW_v7",
            embedding_function=embeddings,
            persist_directory="./chroma_langchain_db",
        )

        if vector_store.get()["documents"]:
            print(f"\nVector Store loaded with: {len(vector_store.get()["documents"])} documents\n")
            return vector_store
        else:
            print(f"\nVector Store is empty. Ending script.\n")
            sys.exit()
    except Exception as error:
        print(f"Error: {error}")
        sys.exit()
