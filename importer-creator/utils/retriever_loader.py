from utils.vectorstore_loader import load_vectorstore


def load_retriever():
    vector_store = load_vectorstore()

    retriever = vector_store.as_retriever(search_type="similarity", k=3)

    return retriever
