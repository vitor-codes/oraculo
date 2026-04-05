import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

# =============================
# CONFIGURAÇÕES
# =============================

TIPOS_ARQUIVOS = ["Site", "PDF", "Csv", "Txt"]

OPENAI_MODELOS = ["gpt-4o-mini", "gpt-4o"]

MAX_HISTORICO = 4  # limite de mensagens no histórico


def openai_api_key() -> str:
    return os.environ.get("OPENAI_API_KEY", "").strip()
