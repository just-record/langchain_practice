# Tutorials - Get Started - Chat models and prompts

<https://python.langchain.com/docs/tutorials/llm_chain/>

## python-dotenv, rich

- python-dotenv: 환경 변수를 쉽게 관리하는 Python 패키지
- rich: 터미널 출력을 보기 좋게 해주는 Python 패키지

```bash
pip install python-dotenv
pip install rich
```

✔️ OpenAI API 키 설정

`.env` 파일 생성하고 아래와 같이 키를 설정합니다.

```text
OPENAI_API_KEY=sk-xxxxxxxxxx
```

✔️ `01.use_dotenv.py`: 확인

## Setup

✔️ LangChain 설치

```bash
pip install langchain
```

✔️ LangSmith

<https://smith.langchain.com/>

`.env` 파일

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=lsv2_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
LANGCHAIN_PROJECT=LANGCHAIN_PRACTICE
```

## Using Language Models

✔️ OpenAI

```bash
pip install -qU langchain-openai
```

- 02.using_language_models_openai.py

✔️ Anthropic

```bash
pip install -qU langchain-anthropic
```

- 03.using_language_models_anthropic.py

## Prompt Templates

- 04.prompt_templates_openai.py: OpenAI
- 05.prompt_templates_anthropic.py: Anthropic