import streamlit as st
import tempfile
import os

from loaders import (
    carregar_site,
    carregar_pdf,
    carregar_csv,
    carregar_txt,
)

from langchain_openai import ChatOpenAI

from vectorstore import criar_vectorstore
from config import MAX_HISTORICO, openai_api_key
from session import criar_sessao


def carregar_arquivo(tipo, arquivo):
    if tipo == "Site":
        return carregar_site(arquivo)

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(arquivo.read())
        path = temp.name

    try:
        if tipo == "PDF":
            return carregar_pdf(path)

        if tipo == "Csv":
            return carregar_csv(path)

        if tipo == "Txt":
            return carregar_txt(path)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def formatar_historico(history):
    historico = history[-MAX_HISTORICO:] #pega os últimos 4 turnos do histórico

    texto = "" #inicia o texto vazio
    for h in historico: #percorre os últimos 4 turnos
        texto += f"Usuário: {h['pergunta']}\n" #adiciona a pergunta do usuário
        texto += f"Assistente: {h['resposta']}\n\n" #adiciona a resposta do assistente

    return texto #retorna o texto formatado


def inicializar_oraculo(modelo, tipo, arquivo):
    api_key = openai_api_key()
    if not api_key:
        st.error("Defina OPENAI_API_KEY no arquivo .env na pasta do projeto.")
        st.stop()

    persist_dir = criar_sessao()
    documento = carregar_arquivo(tipo, arquivo)

    vectordb = criar_vectorstore(
        documento=documento,
        api_key=api_key,
        persist_dir=persist_dir,
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 8})

    llm = ChatOpenAI(model=modelo, api_key=api_key, streaming=True)
    # estado do RAG (retriever + LLM) na sessão Streamlit
    st.session_state.oraculo = {
        "retriever": retriever,
        "llm": llm,
        "persist_dir": persist_dir
    }

    st.session_state.history = [] #zera o histórico


def stream_resposta(oraculo, pergunta): #gera a resposta
    retriever = oraculo["retriever"] #pega o retriever
    llm = oraculo["llm"] #pega o modelo

    docs = retriever.invoke(pergunta) #busca os chunks mais relevantes/semelhantes
    contexto = "\n\n".join([doc.page_content for doc in docs]) #concatena os chunks em um único texto

    historico = formatar_historico(st.session_state.history) #formata o histórico

    prompt = f"""
Você é o assistente de um sistema RAG com memória vetorial.

Histórico recente da conversa:
{historico}

Use PRIORITARIAMENTE as informações abaixo para responder.
Se não encontrar a resposta no material, diga que não encontrou.

###
{contexto}
###

Pergunta atual: {pergunta}
"""

    for chunk in llm.stream(prompt):
        yield chunk.content
