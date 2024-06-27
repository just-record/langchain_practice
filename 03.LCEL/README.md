# LCEL

<https://python.langchain.com/v0.2/docs/how_to/#langchain-expression-language-lcel>

## 01.chain_runnables

- 두 개의 실행 가능 항목을 시퀀스로 함께 연결: '...any two runnables can be "chained" together into sequences...'
- `|` 연산자를 사용 하여 연결
- `.pipe()` 메서드를 사용하여 연결

## 02.stream_runnables

- stream, astream 를 이용하여 출력을 스트리밍하기
- chain과 stream을 함께 사용
- json type의 스트리밍
- 최종 입력값으로 작동하는 체인이 존재하면 스트미링 기능 중단
- yield를 사용 하여 스트리밍이 가능하도록
- 스트리밍이 불가하거나 의미 없는 것 - Some built-in components like Retrievers
- 비스트리밍 단계 이후 부터 스트리밍 가능