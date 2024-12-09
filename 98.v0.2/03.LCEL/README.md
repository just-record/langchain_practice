# LCEL

<https://python.langchain.com/v0.2/docs/how_to/#langchain-expression-language-lcel>

## 01.chain_runnables

- 두 개의 실행 가능 항목을 시퀀스로 함께 연결: '...any two runnables can be "chained" together into sequences...'
- `|` 연산자를 사용 하여 연결
- `.pipe()` 메서드를 사용하여 연결

## 02.stream_runnables

- stream, astream 를 이용하여 출력을 스트리밍하기
- chain과 stream을 함께 사용, json type의 스트리밍
- 최종 입력값으로 작동하는 체인이 존재하면 스트미링 기능 중단
- yield를 사용 하여 스트리밍이 가능하도록
- 스트리밍이 불가하거나 의미 없는 것 - Some built-in components like Retrievers
- 비스트리밍 단계 이후 부터 스트리밍 가능
- Stream Events(베타버전): Chain, model/parset, Filtering, Callbacks 전파

## 03.invoke runnables in parallel

- 'context'와 'question'을 병렬로 실행
- 'itemgetter'와 결합
- RunnableParallels를 사용 하여 병렬로 실행. 단일 실행과 시간 비교

## 04.add default invocation args to a Runnable

- model.bind()를 사용하여 Runnable 내에서 상수 인수를 포함하여 호출하기
- model.bind(tools=) 사용 하여 OpenAI tools 를 첨부

## 05.run custom functions

- RunnableLambda의 생성자에 전달하여 Runnable을 만들기
- '@chain' 데코레이터를 사용하여 chain으로 만들기
- Streamimg - 사용자 정의 출력 파서, 다음 쉼표 생성 하는 사용자 지정 함수 정의, 비동기 버전

## 06.pass through arguments from one step to the next

- 'RunnablePassthrough'를 사용하여 변경 없이 다음 단계로 data 전달하기
- 'Retrieval'에서  'RunnablePassthrough'를 사용 하는 예제

## 07.configure runtime chain internals

- 'configurable_fields'를 사용하여 런타임 시의 체인의 특정 단계에서 매개 변수를 지정하기
  - 'chain'에서 사용, 'prompt' 변경 예시
- 'configurable_alternatives'를 사용하여 대체 단계로 변경 하기 - 'llm'과 'prompt' 변경하기
- configurations를 저장하기

## 08.add message history

- 'RunnableWithMessageHistory'의 기본 사용 법 - session_id, get_session_history() 사용
- 'input_messages_key', 'history_messages_key', 'output_messages_key'의 사용 예시  
- 'input_messages_key'의 특정 사례 - 모든 메시지 입력, 출력을 단위 키로 저장
- Customization - 다 이해 되지 않음

## 09.route between sub-chains

- 'custom function'과 'RunnableLambda'를 사용 하여 sub chain 연결하기 (Recommended)
- 'RunnableBranch'를 사용 하여 sub chain 연결하기 (Legacy)
- embedding을 사용하여 의미적으로 유사한 prompt의 sub chain 연결하기

## 10.create a dynamic chain

- 'RunnablePassthrough.assign'로 입력 데이터를 수정하여 동적 체인 생성하기

## 11.inspect runnables

- get_graph().print_ascii() - runnable의 그래프.  get_prompts() - prompt 확인

## 12.add fallbacks to a runnable

- fallbacks을 적용하여 error 발생 시 다른 모델로 전환
- chain, sequences, long inputs에 적용
- 빠른고 싼 모델에서 실패하면 더 좋은 모델 사용

## Cheatsheet

- 01: runnable invoke 하기
- 02: runnable batch 하기
- 03: runnable stream 하기 - yield 사용
- 04: runnable을 compose 하기 - '|', 'parallel' 사용
- 05: 'RunnableLambda'로 일반 함수를 runnable로 만들기
- 06: 'RunnablePassthrough'로 입력을 그대로 전달하기. 'RunnablePassthrough.assign'로 기존 입력에 새로운 키-값 쌍을 추가하기
- 07: 'RunnablePassthrough'로 입력을 그대로 전달하기
- 08: 'bind'를 이용 하여 Runnable 객체에 부분적으로 인자를 미리 지정하기
- 09: fallbacks 적용 - 'runnable1.with_fallbacks([runnable2])'
- 10: retry 적용 - 'runnable..with_retry(stop_after_attempt=2)'
- 11: 'RunnableConfig'를 사용 하여 runnable객체의 세부적인 실행 방식을 동적으로  조정
- 12: 'Runnable.with_config'를 사용하여 초기 값 설정
- 13: 'configurable_fields'를 이용 하여 설정 가능한 속성을 설정하기
- 14: 'configurable_alternatives'를 이용 하여 설정 가능한 대체 구성 요소를 설정하기
- 15: 입력 값에 의해 동적인 체인 생성 하기
- 16: 이벤트 스트림 생성 하기
- 17: 'batch_as_completed' - 입력 리스트의 각 요소를 병렬로 처리
- 18: 'runnable.pick' - 출력의 일부만 반환
- 19: 'runnable.map()' - 입력 컬렉션의 각 요소에 대해 Runnable을 실행
- 20: 'chain.get_graph().print_ascii()'로 그래프 출력
- 21: 'chain.get_prompts()'로 모든 prompt 확인
- 22: 'with_listeners' - 실행 시 특정 이벤트가 발생할 때 호출되는 콜백 함수를 추가
