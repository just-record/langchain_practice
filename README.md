# langchain_practice

<https://python.langchain.com/v0.2/docs/how_to/>

LangChain 공식 문서를 따라하며 연습하는 저장소입니다. OpenAI API를 중심으로 합니다.

## Installation

`requirements.txt`

```text
langchain
langchain-core
langchain-community
langchain-experimental
langsmith
python-dotenv
langchain-openai
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

pass

### Example selectors

pass

### Chat models

pass

### Messages

pass

### LLMs

pass

### Output parsers

pass

### Document loaders

pass

### Text splitters

pass

### Embedding models

pass

### Vector stores

pass

### Retrievers

pass

### Indexing

pass

### Tools

pass

### Multimodal

pass

### Agent

pass

### Callbacks

pass

### Custom

pass

### Serialization

pass

## Use cases

### Q&A with RAG

pass

### Extraction

pass

### Chatbots

pass

### Query analysis

pass

### Q&A over SQL + CSV

pass

### Q&A over graph databases

pass