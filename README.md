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
faiss-cpu
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

03.LCEL - 연습 중

## Components

04.Components

### Pormpt templates

TODO

### Example selectors

TODO

### Chat models

TODO

### Messages

TODO

### LLMs

TODO

### Output parsers

TODO

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

TODO

### Multimodal

TODO

### Agent

TODO

### Callbacks

TODO

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