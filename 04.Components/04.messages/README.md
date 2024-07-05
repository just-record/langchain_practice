# Messages

<https://python.langchain.com/v0.2/docs/how_to/#messages>

## Messages

<https://python.langchain.com/v0.2/docs/concepts/#messages>

읽어 볼 것: role, content / HumanMessage, AIMessage(response_metadata, tool_calls), SystemMessage, FunctionMessage, ToolMessage

## How to

### How to trim messages

<https://python.langchain.com/v0.2/docs/how_to/trim_messages/>

- 01.trim_messages_last_first.py: 'trim_messages' - 모델의 max_tokens에 맞게 메시지 자르기 - last: 최근 메시지가 남도록, first: 처음 메시지가 남도록
- 02.custom_token.counter.py: 사용자 정의 토큰 카운터 - 이런게 있다 정도만 알아 두자
- 03.trim_messages_chaining.py: 'trim_messages'를 chain에 조합하기
- 04.use_with_chatmessagehistory.py: 
  - 'InMemoryChatMessageHistory': 메모리상에 대화 history를 저장. 프로그램이 종료 되면 지워 짐. 대량의 대화 기록 사용은 주의
  - 'RunnableWithMessageHistory': 대화 기록을 유지하면서 AI 모델이나 체인(chain)을 실행. 세션별로 독립적인 대화 기록을 관리함

### How to filter messages

<https://python.langchain.com/v0.2/docs/how_to/filter_messages/>

- 05.filter_messages.py: 'filter_messages' - 메시지 필터링

### How to merge consecutive messages of the same type

<https://python.langchain.com/v0.2/docs/how_to/merge_message_runs/>

- 06.merge_message_sametype.py: 'merge_message_runs' - 연속된 동일한 유형의 메시지 병합하기
  - 'chaining' - OpenAI는 오류, Anthropic은 잘 됨. - Anthropic api key 발급 문제로 예제를 하지 않으려 했으나 지금 부터 해 봐야 할 듯 함