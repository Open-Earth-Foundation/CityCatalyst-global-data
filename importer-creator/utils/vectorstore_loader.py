import sys
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from utils.config_loader import ConfigLoader

load_dotenv()


def load_vectorstore():
    try:
        print("\nLoading vector store\n")

        # Get configuration
        embeddings_model = ConfigLoader.get_embeddings_model()
        base_url = ConfigLoader.get_base_url()
        api_key = ConfigLoader.get_api_key()

        # Create embeddings model with OpenRouter
        embeddings = OpenAIEmbeddings(
            model=embeddings_model,
            base_url=base_url,
            api_key=api_key  # type: ignore
        )

        # Create Chroma vector store
        vector_store = Chroma(
            collection_name="GPC_Full_MASTER_RW_v7",
            embedding_function=embeddings,
            persist_directory="./chroma_langchain_db",
        )

        if vector_store.get()["documents"]:
            print(
                f"\nVector Store loaded with: {len(vector_store.get()['documents'])} documents\n"
            )
            return vector_store
        else:
            print(f"\nVector Store is empty. Ending script.\n")
            sys.exit()
    except Exception as error:
        print(f"Error: {error}")
        sys.exit()
