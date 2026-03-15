from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


def criar_vectorstore(documento, api_key, persist_dir):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500
    )# divide o documento em chunks

    textos = splitter.split_text(documento) #quebra o documento em chunks

    embeddings = OpenAIEmbeddings(
        api_key=api_key
    )

    vectordb = Chroma.from_texts(
        texts=textos,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    return vectordb
