from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=800,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

file_path = "../files/GPC_Full_MASTER_RW_v7.pdf"

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
    persist_directory="../chroma_langchain_db",
)

# Add documents to vector store
vector_store.add_documents(pages)

print(vector_store.similarity_search("What is GPC"))

# Create Chroma vector database
# vector_db = Chroma.from_documents(pages, embeddings)


# print(vector_db.similarity_search("What is GPC"))
