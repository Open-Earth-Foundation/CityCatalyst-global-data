from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from utils.config_loader import ConfigLoader

load_dotenv()


def create_vectorstore():
    print("\nCreating Vector Store\n")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        is_separator_regex=False,
    )

    file_path = "./files/GPC_Full_MASTER_RW_v7.pdf"

    # Load PDF file
    loader = PyPDFLoader(file_path)

    # Split PDF using text splitter
    pages = loader.load_and_split(text_splitter)

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

    # Add documents to vector store
    vector_store.add_documents(pages)

    print(
        f"\nVector Store created with {len(vector_store.get()['documents'])} documents.\n"
    )


if __name__ == "__main__":
    create_vectorstore()
