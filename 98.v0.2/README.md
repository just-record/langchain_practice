# LangChain v0.2

## Installation

`requirements.txt`

```text
langchain
langchain-core
langchain-community
langchain-experimental
langchain-openai
langchainhub
langchain_anthropic
langchain-huggingface
langsmith
langgraph
grandalf
python-dotenv
faiss-cpu
langchain_chroma
nltk
wikipedia
```

Installation

```bash
pip install -r requirements.txt
```

### OpenAI API 키 설정

`.env` 파일 생성하고 아래와 같이 키를 설정합니다.

```text
OPENAI_API_KEY=sk-xxxxxxxxxx
```

확인: 01.Installation의 `01.use_dotenv.py`를 실행합니다.

```bash
cd 01.Installation
python 01.use_dotenv.py
```

## Key Features

TODO: 다른 파트 연습 후에 볼 것

- How to: return structured data from a model
- How to: use a model to call tools
- How to: stream runnables
- How to: debug your LLM apps

## LCEL(LangChain Expression Language)

03.LCEL

## Components

04.Components

### Pormpt templates

- 01.pormpt_templates

### Example selectors

- 02.example_selectors

### Chat models

- 03.chat_models

### Messages

- 04.messages

### LLMs

- 05.LLMs

### Output parsers

- 06.output_parsers

### Document loaders

TODO

### Text splitters

TODO

### Embedding models

TODO

### Vector stores

TODO

### Retrievers

TODO

### Indexing

TODO

### Tools

- 13.tools

### Multimodal

-14.multimodal

### Agent

- 15.agent

### Callbacks

- 16.callbacks

### Custom

TODO

### Serialization

TODO

## Use cases

### Q&A with RAG

TODO

### Extraction

TODO

### Chatbots

TODO

### Query analysis

TODO

### Q&A over SQL + CSV

TODO

### Q&A over graph databases

TODO