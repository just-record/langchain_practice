# How-to guides - Key features - How to debug your LLM apps

<https://python.langchain.com/docs/how_to/debugging/>

## Tracing

✔️ LangSmith

<https://smith.langchain.com/>

- 회원가입
  - Create an account -> Continue with Google -> 계정 선택
- 로그인
  - 로그인 -> Get started -> Generate API key -> API key 복사
- 환경변수 설정
  - `.env` 파일에 아래 내용 추가

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="lsv2_xxxxxxxxx"
LANGCHAIN_PROJECT="LangChain-practice"
```

✔️ Tavily Search

<https://tavily.com/>

- Sign up
  - Sign up -> Continue with Google -> Google 계정 선택 -> 계정 선택
- Log in
  - API-KEY 복사
- 환경변수 설정
  - `.env` 파일에 아래 내용 추가

```bash
TAVILY_API_KEY="xxxxxxxxx"
```

- 01.tracing.py
  - <https://smith.langchain.com/public/a89ff88f-9ddc-4757-a395-3a1b365655bf/r>: 공식 문서에서 제공하는 URL

## `set_debug` and `set_verbose`

- 02.set_verbose.py
- 03.set_debug.py

