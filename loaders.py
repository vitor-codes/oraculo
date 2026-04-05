from langchain_community.document_loaders import (
    WebBaseLoader,
    PyPDFLoader,
    CSVLoader,
    TextLoader,
)

import os
from fake_useragent import UserAgent
import streamlit as st
from time import sleep


def carregar_site(url):
    documento = ""
    for _ in range(5):
        try:
            os.environ["USER_AGENT"] = UserAgent().random
            loader = WebBaseLoader(url, raise_for_status=True)
            docs = loader.load()
            documento = "\n\n".join([doc.page_content for doc in docs])
            break
        except Exception as e:
            sleep(2)

    if not documento:
        st.error("Não foi possível carregar o site. Verifique a URL e tente novamente.")
        st.stop()

    return documento


def carregar_pdf(path):
    try:
        loader = PyPDFLoader(path)
        docs = loader.load()
        if not docs:
            st.error("Não foi possível extrair conteúdo do PDF.")
            st.stop()
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        st.error(f"Erro ao carregar PDF: {e}")
        st.stop()


def carregar_csv(path):
    try:
        loader = CSVLoader(path)
        docs = loader.load()
        if not docs:
            st.error("Não foi possível extrair conteúdo do CSV.")
            st.stop()
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        st.error(f"Erro ao carregar CSV: {e}")
        st.stop()


def carregar_txt(path):
    try:
        loader = TextLoader(path)
        docs = loader.load()
        if not docs:
            st.error("Não foi possível extrair conteúdo do arquivo TXT.")
            st.stop()
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        st.error(f"Erro ao carregar TXT: {e}")
        st.stop()
