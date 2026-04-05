import streamlit as st

try:
    from config import OPENAI_MODELOS, TIPOS_ARQUIVOS, openai_api_key
except ModuleNotFoundError as e:
    raise SystemExit(
        "Pacotes do projeto não estão neste Python. Na pasta do projeto execute:\n"
        "  uv sync\n"
        "  uv run streamlit run app.py\n"
        "Ou dê duplo clique em run.bat"
    ) from e
from rag import inicializar_oraculo, stream_resposta
from session import (
    remover_sessao,
    ensure_multi_session_state,
    persist_active_session,
    register_session,
    activate_session,
)


def _rotulo_sessao(tipo, arquivo):
    if tipo == "Site":
        s = (arquivo or "").strip()
        return (s[:50] + "…") if len(s) > 50 else (s or "Site")
    if arquivo is not None and hasattr(arquivo, "name"):
        n = str(arquivo.name)
        return (n[:50] + "…") if len(n) > 50 else n
    return tipo


st.set_page_config(page_title="RAG com memória vetorial", layout="wide")
st.title("RAG com memória vetorial")

with st.sidebar:
    st.header("⚙️ Configurações")
    ensure_multi_session_state()

    ids_sessoes = list(st.session_state.rag_sessions.keys())
    if ids_sessoes:
        if st.session_state.rag_current_session_id not in st.session_state.rag_sessions:
            activate_session(ids_sessoes[0])
        idx = ids_sessoes.index(st.session_state.rag_current_session_id)
        escolha = st.selectbox(
            "Navegar entre sessões",
            options=ids_sessoes,
            index=idx,
            format_func=lambda sid: st.session_state.rag_sessions[sid]["label"],
            key="rag_sel_sessao",
        )
        if escolha != st.session_state.rag_current_session_id:
            activate_session(escolha)
            st.rerun()

    tipo = st.selectbox("Tipo de arquivo", TIPOS_ARQUIVOS)

    if tipo == "Site":
        arquivo = st.text_input("URL")
    else:
        arquivo = st.file_uploader("Upload", type=tipo.lower())

    modelo = st.selectbox("Modelo (OpenAI)", OPENAI_MODELOS)
    if openai_api_key():
        st.caption("Chave OpenAI carregada do arquivo `.env`.")
    else:
        st.warning("Defina `OPENAI_API_KEY` no arquivo `.env`.")

    if st.button("🚀 Inicializar RAG com memória vetorial"):
        if not arquivo:
            st.error("Preencha o arquivo ou a URL.")
        elif not openai_api_key():
            st.error("Defina OPENAI_API_KEY no arquivo .env.")
        else:
            persist_active_session()
            inicializar_oraculo(modelo, tipo, arquivo)
            register_session(_rotulo_sessao(tipo, arquivo))
            st.success("RAG com memória vetorial inicializado!")

    if st.button("🧹 Limpar Histórico"):
        st.session_state.history = []
        persist_active_session()

    if st.button("🗑️ Remover Sessão"):
        remover_sessao()
        st.success("Sessão removida!")


if "oraculo" not in st.session_state:
    st.info("Inicialize o RAG com memória vetorial no menu lateral.")
else:
    for h in st.session_state.history:
        with st.chat_message("user"):
            st.markdown(h["pergunta"])

        with st.chat_message("assistant"):
            st.markdown(h["resposta"])

    pergunta = st.chat_input("Pergunta")

    if pergunta:
        with st.chat_message("user"):
            st.markdown(pergunta)

        with st.chat_message("assistant"):
            resposta = st.write_stream(
                stream_resposta(
                    st.session_state.oraculo,
                    pergunta
                )
            )

        st.session_state.history.append({
            "pergunta": pergunta,
            "resposta": resposta
        })
        persist_active_session()
