# RAG com memória vetorial

Aplicação web interativa construída com Streamlit que implementa RAG (Retrieval-Augmented Generation) com memória vetorial. Permite conversar com modelos OpenAI sobre diferentes tipos de documentos usando busca semântica para recuperar informações relevantes.

## ✨ Funcionalidades

- **RAG com Memória Vetorial:**
  - Armazenamento vetorial com ChromaDB
  - Busca semântica de informações relevantes
  - Recuperação dos 8 chunks mais relevantes para cada pergunta
  - Persistência de sessões de conversa

- **Múltiplos tipos de documentos suportados:**
  - 📄 Sites (URLs)
  - 📑 Arquivos PDF
  - 📊 Arquivos CSV
  - 📝 Arquivos de texto (TXT)

- **OpenAI:**
  - Modelos de chat GPT-4o e GPT-4o-mini
  - Embeddings e chave de API via arquivo `.env` (`OPENAI_API_KEY`)

- **Interface intuitiva:**
  - Chat interativo com histórico de conversas (últimos 4 turnos)
  - Sidebar para configuração e upload
  - Streaming de respostas em tempo real
  - Limpeza de memória do chat
  - Remoção de sessões e vetores

## 📋 Pré-requisitos

- Python 3.8 ou superior
- OpenAI API Key (chat e embeddings), definida no arquivo `.env` como `OPENAI_API_KEY=...`

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/DSagentpy/oraculo.git
cd oraculo
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📦 Dependências

O projeto utiliza as seguintes bibliotecas principais:

- `streamlit` - Framework para aplicações web
- `langchain` - Framework para aplicações com LLMs
- `langchain-community` - Loaders de documentos da comunidade
- `langchain-openai` - Integração com OpenAI e embeddings
- `chromadb` - Banco de dados vetorial (via langchain-community)
- `fake_useragent` - Geração de User-Agents aleatórios
- `pypdf` - Processamento de PDFs
- `bs4` - Parsing de HTML
- `unstructured` - Processamento de documentos não estruturados
- `python-dotenv` - Gerenciamento de variáveis de ambiente

## 🎯 Como Usar

1. **Inicie a aplicação:**
```bash
streamlit run app.py
```

2. **Crie o arquivo `.env` na raiz do projeto** com sua chave:
   ```
   OPENAI_API_KEY=sua_chave_aqui
   ```
3. **Configure o RAG com memória vetorial:**
   - Na sidebar, selecione o tipo de arquivo (Site, PDF, Csv ou Txt)
   - Se for Site, forneça a URL
   - Se for PDF, CSV ou TXT, faça upload do arquivo
   - Escolha o modelo OpenAI desejado
   - Clique em "🚀 Inicializar RAG com memória vetorial"

4. **Comece a conversar:**
   - Digite suas perguntas no campo de chat
   - O sistema buscará informações relevantes no documento usando busca semântica
   - A resposta será gerada com base no contexto recuperado
   - Use "🧹 Limpar Histórico" para resetar o histórico de conversas
   - Use "🗑️ Remover Sessão" para remover a sessão e os vetores armazenados

## 🏗️ Arquitetura RAG

O projeto implementa RAG (Retrieval-Augmented Generation) da seguinte forma:

1. **Carregamento de Documentos:** Os documentos são carregados usando loaders específicos
2. **Divisão em Chunks:** O texto é dividido em chunks de 2000 caracteres com overlap de 500
3. **Geração de Embeddings:** Cada chunk é convertido em vetor usando OpenAI Embeddings
4. **Armazenamento Vetorial:** Os vetores são armazenados no ChromaDB
5. **Recuperação:** Para cada pergunta, os 8 chunks mais relevantes são recuperados
6. **Geração:** O LLM gera a resposta usando o contexto recuperado e o histórico da conversa

## 📁 Estrutura do Projeto

```
RAG/
├── app.py              # Aplicação principal Streamlit
├── rag.py              # Lógica RAG (inicialização e geração de respostas)
├── config.py           # Configurações (modelos, tipos de arquivos)
├── loaders.py          # Funções para carregar diferentes tipos de documentos
├── vectorstore.py      # Criação e gerenciamento do vectorstore
├── session.py          # Gerenciamento de sessões e persistência
├── requirements.txt    # Dependências do projeto
└── README.md           # Este arquivo
```

## 🔧 Arquivos Principais

### `app.py`
Aplicação principal que contém:
- Interface Streamlit
- Gerenciamento de estado (histórico de chat, retriever/LLM)
- Inicialização de modelos de IA
- Interface de chat interativa com streaming

### `rag.py`
Módulo com a lógica RAG:
- `inicializar_oraculo()` - Carrega documento, cria vectorstore e prepara o RAG na sessão
- `stream_resposta()` - Gera respostas usando RAG com streaming
- `formatar_historico()` - Formata o histórico de conversas (últimos 4 turnos)
- `carregar_arquivo()` - Roteia para o loader apropriado

### `config.py`
Configurações centralizadas:
- Tipos de arquivos suportados
- Lista de modelos OpenAI e leitura de `OPENAI_API_KEY` do `.env`
- Limite de histórico de conversas

### `loaders.py`
Módulo com funções para carregar diferentes tipos de documentos:
- `carregar_site()` - Carrega conteúdo de URLs (com retry e User-Agents aleatórios)
- `carregar_pdf()` - Processa arquivos PDF
- `carregar_csv()` - Processa arquivos CSV
- `carregar_txt()` - Processa arquivos de texto

### `vectorstore.py`
Criação do vectorstore:
- `criar_vectorstore()` - Divide documentos, gera embeddings e cria vectorstore ChromaDB

### `session.py`
Gerenciamento de sessões:
- `criar_sessao()` - Cria uma nova sessão com ID único
- `remover_sessao()` - Remove sessão e limpa vetores armazenados

## 💡 Exemplos de Uso

### Carregar um site
1. Selecione "Site" como tipo de arquivo
2. Digite a URL: `https://exemplo.com`
3. Configure o modelo OpenAI
4. Inicialize o RAG com memória vetorial (chave no `.env`)
5. Faça perguntas sobre o conteúdo do site

### Carregar um PDF
1. Selecione "PDF" como tipo de arquivo
2. Faça upload do arquivo PDF
3. O conteúdo será processado e indexado vetorialmente
4. Faça perguntas sobre o conteúdo do PDF

## ⚙️ Configuração

O app suporta os seguintes modelos:

**OpenAI (chat e embeddings):**
- `gpt-4o-mini`
- `gpt-4o`

**Embeddings:**
- OpenAI Embeddings (usado para todos os casos)

**Parâmetros RAG:**
- Tamanho do chunk: 2000 caracteres
- Overlap: 500 caracteres
- Número de chunks recuperados (k): 8
- Histórico de conversas: últimos 4 turnos

## 🔒 Segurança

- A chave OpenAI fica no arquivo `.env` (não versionado no git); não a compartilhe
- Arquivos temporários são criados durante o processamento e podem ser limpos após o uso
- Sessões são isoladas por ID único
- Vetores são armazenados localmente no diretório `chromadb/`

## 🐛 Solução de Problemas

- **Erro ao carregar site:** O carregador tenta obter o site até 5 vezes com User-Agents aleatórios. Se falhar, verifique se a URL está correta e acessível.
- **Erro de API Key:** Confira se `OPENAI_API_KEY` está definida no `.env` na pasta do projeto e se a chave é válida na OpenAI.
- **Memória insuficiente:** Para documentos muito grandes, considere dividir em partes menores.
- **Sessão não removida:** Use o botão "🗑️ Remover Sessão" para limpar os vetores armazenados.

## 📝 Notas

- O histórico de conversas mantém os últimos 4 turnos para contexto
- Cada nova inicialização do RAG cria uma nova sessão de índice e histórico de chat associado
- Os vetores são persistidos no diretório `chromadb/` (não versionado no git)
- O sistema usa streaming para respostas em tempo real

## 🤝 Contribuindo

Sinta-se à vontade para abrir issues ou pull requests para melhorias!

## 📄 Licença

Este projeto é de uso educacional.

---
