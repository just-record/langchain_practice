# stream runnables

<https://python.langchain.com/v0.2/docs/how_to/streaming/>

- 01.stream_runnables.py: stream API - sync (model.stream() - 단계없이)
- 02.stream_runnables.py: astream API - async (model.astream() - 단계없이)
- 03.stream_runnables.py: (prompt | model | parser).astream() - 여러 단계로
- 04.stream_runnables.py: stream - json type (JsonOutputParser)
- 05.stream_runnables.py: 스트리밍 기능 중단 - 최종 입력값으로 작동하는 체인이 존재하면
- 06.stream_runnables.py: a generator function(a function that uses yield) - 스트리밍이 가능
- 07.stream_runnables.py: 스트리밍이 불가하거나 의미 없는 것도 있다 - Some built-in components like Retrievers
- 08.stream_runnables.py: 비스트리밍 단계 이후 부터 스트리밍 가능
- 09.stream_runnables.py: Stream Events - Beta
- 10.stream_runnables.py: Chain에서의 Stream Events
- 11.stream_runnables.py: 모델과 파서의 Stream Events
- 12.stream_runnables.py: Stream Events의 필터링 - By name, By type, By tags
- 13.stream_runnables.py: 05.stream_runnables.py의 최종 입력값으로 작동하는 체인이 존재하여 스트리밍이 기능이 중단되어도 스트림 이벤트는 계속 발생
- 14.stream_runnables.py: Callbacks 전파 - tool내에서 Runnables를 invoke할 때 콜백을 전파하지 않으면 스트림 이벤트가 생성 되지 않음. bad_tool과 correct_tool의 차이를 모르겠음
- 15.stream_runnables.py: Runnable Lambdas 또는 @chain을 쓰면 Callbacks이 자동으로 전파

## 추가 분석

- JsonOutputParser
- RunnablePassthrough
- FAISS
- OpenAIEmbeddings
- RunnableLambda
- tool
- chain