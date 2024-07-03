# LangChain Expression Language Cheatsheet

<https://python.langchain.com/v0.2/docs/how_to/lcel_cheatsheet/>

- 01.invoke_a_runnable.py: runnable invoke 하기
- 02.batch_a_runnable.py: runnable batch 하기
  - 추가로 llm 까지 연결
- 03.stream_a_runnable: runnable stream 하기 - yield 사용
- 04.compose_runnables_01_pipe.py: runnable을 compose 하기 - '|' 사용
- 04.compose_runnables_02_parallel.py: runnable을 compose 하기 - 'parallel' 사용
- 05.turn_any_function_into_a_runnable.py: 'RunnableLambda'로 일반 함수를 runnable로 만들기
- 06.merge_input_and_output_dicts.py: 'RunnablePassthrough'로 입력을 그대로 전달하기. 'RunnablePassthrough.assign'로 기존 입력에 새로운 키-값 쌍을 추가하기
- 07.include_input_dict_in_output_dict.py: 'RunnablePassthrough'로 입력을 그대로 전달하기
- 08.add_default_invocation_args.py: 'bind'를 이용 하여 Runnable 객체에 부분적으로 인자를 미리 지정하기
- 09.add_fallbacks.py: fallbacks 적용 - 'runnable1.with_fallbacks([runnable2])'
- 10.add_retries_01_origin.py: retry 적용 - 'runnable..with_retry(stop_after_attempt=2)'
- 10.add_retries_02_test.py: 공식 예제 외에 retry 추가 test
- 11.configure_runnable_execution.py: 'RunnableConfig'를 사용 하여 runnable객체의 세부적인 실행 방식을 동적으로  조정
- 12.add_default_config_to_runnable.py: 'Runnable.with_config'를 사용하여 초기 값 설정. 초기 값이 설정 된 runnable를 따로 저장 가능
  - 11.configure_runnable_execution.py과 차이: 11.은 invoke시에 동적으로 설정, 12.는 초기 값 설정
  - 공식 예제에서 병렬 실행에 관한 설정이라 눈으로 직접 확인은 불가
- 13.make_runnable_attributes_configurable.py: 'configurable_fields'를 이용 하여 설정 가능한 속성을 설정하기
  - 'FooRunnable'는 runnable객체 class - 자세히 이해 하려고 하지 말고 'output_key'속성이 있고 설정 가능하다는 것만 이해
  - <https://github.com/just-record/langchain_practice/tree/main/03.LCEL/07.configure_runtime_chain_internals> 참조
- 14.make_chain_components_configurable.py: 'configurable_alternatives'를 이용 하여 설정 가능한 대체 구성 요소를 설정하기
  - <https://github.com/just-record/langchain_practice/tree/main/03.LCEL/07.configure_runtime_chain_internals> 참조
- 15.build_a_chain_dynamically_based_on_input.py: 입력 값에 의해 동적인 체인 생성 하기
- 16.generate_a_stream_of_events.py: 이벤트 스트림 생성 하기
  - <https://github.com/just-record/langchain_practice/tree/main/03.LCEL/02.stream_runnables>: 09.stream_runnables.py 참조
- 17.yield_batched_outputs_as_they_complete.py: 'batch_as_completed' - 입력 리스트의 각 요소를 병렬로 처리
- 18.return_subset_of_output_dict.py: 'runnable.pick' - 출력의 일부만 반환
- 19.declaratively_make_a_batched_version_of_a_runnable.py: 'runnable.map()' - 입력 컬렉션의 각 요소에 대해 Runnable을 실행
- 20.get_a_graph_representation_of_a_runnable.py: 'chain.get_graph().print_ascii()'로 그래프 출력
- 21.get_all_prompts_in_a_chain.py: 'chain.get_prompts()'로 모든 prompt 확인
  - 공식 예제에서 'prompt1.assign(ai_output=fake_llm)'가 제대로 이해 되지 않아(invoke시에 오류 발생) 코드를 수정 해 봄
- 22.add_lifecycle_listeners.py: 'with_listeners' - 실행 시 특정 이벤트가 발생할 때 호출되는 콜백 함수를 추가
