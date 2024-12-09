# configure runtime chain internals

<https://python.langchain.com/v0.2/docs/how_to/configure/>

- 01.configure_runtime_chain.py: 'configurable_fields'를 사용하여 런타임 시의 체인의 특정 단계에서 매개 변수를 지정하기
- 02.configure_runtime_chain.py: 'chain'에서 'configurable_fields'를 사용하기
- 03.configure_runtime_chain.py: 'configurable_fields'를 사용하여 prompt 변경하기 - 'HubRunnable'를 사용하여 hub에서 prompt 가져 옴
- 04.configure_runtime_chain.py: 'configurable_alternatives'를 사용하여 대체 단계로 변경 하기 - 'llm' 변경하기
  - 공식예제는 'Anthropic'과 'OpenAI'를 사용하였으나 여기에서는 'OpenAI'만 사용('gpt-3.5-turbo', 'gpt-4', 'gpt-4o')
- 05.configure_runtime_chain.py: 'configurable_alternatives'를 사용하여 대체 단계로 변경 하기 - 'prompt' 변경하기
- 06.configure_runtime_chain.py: 'configurable_alternatives'를 사용하여 대체 단계로 변경 하기 - 'llm'과 'prompt' 변경하기
- 07.configure_runtime_chain.py: configurations를 저장하기

## 추가 분석

- HubRunnable