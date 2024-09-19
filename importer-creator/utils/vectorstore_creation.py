from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

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

    # Add documents to vector store
    vector_store.add_documents(pages)

    print(f"\nVector Store created with {len(vector_store.get()["documents"])} documents.\n")


if __name__ == "__main__":
    create_vectorstore()
