import streamlit as st
import uuid  # gerar um id único para cada mensagem
import shutil  # copiar arquivos temporários para o diretório de saída
import os


def criar_sessao():
    session_id = str(uuid.uuid4())
    persist_dir = f"./chromadb/{session_id}"
    return persist_dir


def _session_id_from_persist_dir(persist_dir: str) -> str:
    return os.path.basename(os.path.normpath(persist_dir))


def ensure_multi_session_state():
    if "rag_sessions" not in st.session_state:
        st.session_state.rag_sessions = {}
    if "rag_current_session_id" not in st.session_state:
        st.session_state.rag_current_session_id = None


def persist_active_session():
    ensure_multi_session_state()
    cid = st.session_state.get("rag_current_session_id")
    if not cid or "oraculo" not in st.session_state:
        return
    prev = st.session_state.rag_sessions.get(cid, {})
    st.session_state.rag_sessions[cid] = {
        "oraculo": st.session_state.oraculo,
        "history": list(st.session_state.get("history", [])),
        "label": prev.get("label", cid[:8]),
    }


def register_session(label: str):
    ensure_multi_session_state()
    if "oraculo" not in st.session_state:
        return
    cid = _session_id_from_persist_dir(st.session_state.oraculo["persist_dir"])
    st.session_state.rag_sessions[cid] = {
        "oraculo": st.session_state.oraculo,
        "history": list(st.session_state.get("history", [])),
        "label": label,
    }
    st.session_state.rag_current_session_id = cid


def activate_session(session_id: str):
    ensure_multi_session_state()
    if session_id not in st.session_state.rag_sessions:
        return
    old_id = st.session_state.get("rag_current_session_id")
    if old_id and old_id != session_id:
        persist_active_session()
    data = st.session_state.rag_sessions[session_id]
    st.session_state.rag_current_session_id = session_id
    st.session_state.oraculo = data["oraculo"]
    st.session_state.history = list(data.get("history", []))


def remover_sessao():
    ensure_multi_session_state()
    cid = st.session_state.get("rag_current_session_id")

    persist_dir = None
    if cid and cid in st.session_state.rag_sessions:
        data = st.session_state.rag_sessions.pop(cid)
        persist_dir = data["oraculo"].get("persist_dir")
    elif "oraculo" in st.session_state:
        persist_dir = st.session_state.oraculo.get("persist_dir")
        orphan_id = _session_id_from_persist_dir(persist_dir) if persist_dir else None
        if orphan_id and orphan_id in st.session_state.rag_sessions:
            st.session_state.rag_sessions.pop(orphan_id, None)

    if persist_dir and os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    st.session_state.pop("oraculo", None)
    st.session_state.pop("history", None)
    st.session_state.rag_current_session_id = None

    st.session_state.pop("rag_sel_sessao", None)

    remaining = list(st.session_state.rag_sessions.keys())
    if remaining:
        activate_session(remaining[0])