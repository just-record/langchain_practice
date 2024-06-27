# stream runnables

<https://python.langchain.com/v0.2/docs/how_to/streaming/>

- 01.stream_runnables.py: stream API - sync (model.stream() - 단계없이)
- 02.stream_runnables.py: astream API - async (model.astream() - 단계없이)
- 03.stream_runnables.py: (prompt | model | parser).astream() - 여러 단계로
- 04.stream_runnables.py: stream - json type (JsonOutputParser)
- 05.stream_runnables.py: 스트미링 기능 중단 - 최종 입력값으로 작동하는 체인이 존재하면
- 06.stream_runnables.py: a generator function(a function that uses yield) - 스트리밍이 가능
- 07.stream_runnables.py: 스트리밍이 불가하거나 의미 없는 것도 있다 - Some built-in components like Retrievers
- 08.stream_runnables.py: 비스트리밍 단계 이후 부터 스트리밍 가능

## 추가 분석

- JsonOutputParser
- RunnablePassthrough
- FAISS
- OpenAIEmbeddings