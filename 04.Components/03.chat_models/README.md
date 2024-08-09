# Chat models

<https://python.langchain.com/v0.2/docs/how_to/#chat-models>

## Chat Models

<https://python.langchain.com/v0.2/docs/concepts/#chat-models>

한 번 읽어 볼 필요가 있음

### langchain-openai, langchain-anthropic, langchain-community

#### 자체 통합 패키지: langchain-openai, langchain-anthropic

- 특정 제공업체(OpenAI, Anthropic)의 모델에 최적화된 통합을 제공
- 해당 제공업체의 최신 API 변경사항과 기능을 신속하게 반영
- LangChain에서 정의한 표준 매개변수(예: temperature, max_tokens 등)를 엄격하게 준수

#### langchain-community

- 다양한 오픈소스 및 커뮤니티 기반 모델들에 대한 통합을 제공
- 업데이트는 커뮤니티 기여에 크게 의존하며, 업데이트 주기가 다양
- 표준 매개변수를 권장하지만, 모든 통합에서 엄격하게 적용되지는 않을 수 있음

#### 코드 예시

- 00.01.integration_packages_openai.py: 자체 통합 패키지 사용하기 - langchain-openai
- 00.02.integration_packages_antropic.py: 자체 통합 패키지 사용하기 - langchain-anthropic
- 00.03.langchain-community.py: langchain-community => TODO (최신 버전으로 update 필요)

## How to

### How to use a model to call tools

<https://python.langchain.com/v0.2/docs/how_to/tool_calling/>

간단히 읽어 볼 것

- 01.passing_tools_to_chat_models.py: '@tool', 'langchain_core.pydantic_v1' - 사용자 정의 tool 정의 하기
  - 'llm.bind_tools(tools)', 'llm_with_tools.invoke(query).tool_calls'

### How to return structured data from a model

<https://python.langchain.com/v0.2/docs/how_to/structured_output/>

#### The .with_structured_output() method

- 02.structured_output_pydantic.py: 구조화된 데이터를 반환하기 - 'PydanticModel'
- 03.structured_output_json.py: 구조화된 데이터를 반환하기 - 'json'
- 04.structured_output_multiple.py: 2개의 구조 중 질의와 관련 된 구조를 선택 하여 반환하기
- 05.structured_output_stream.py: 구조화된 데이터를 스트리밍 하기
- 06.structured_output_fewshot.py: Few-shot example을 사용하여 구조화된 데이터를 반환하기
- 07.structured_output_fewshot_toolcalls.py: Few-shot example(tool calls)을 사용하여 구조화된 데이터를 반환하기
- 08.structured_output_jsonmode.ppy: 'json_mode'를 사용하여 구조화된 데이터를 반환하기
- 09.structured_output_rawoutputs.py: raw output 반환하기

#### Prompting and parsing model outputs directly

특정 형식을 사용하도록 직접 메시지를 표시하고 출력 파서를 사용하여 원시 모델 출력에서 구조화된 응답을 추출하기

- 10.prompt_parse_output.py: 'PydanticOutputParser'를 사용하여 구조화된 데이터를 반환하기
- 11.prompt_parse_output_custom_parsing.py: 사용자 prompt와 parser를 사용하여 구조화된 데이터를 반환하기
  - 잘 안됨. 나중에 필요 시 다시 분석
 
### How to cache chat model responses

<https://python.langchain.com/v0.2/docs/how_to/chat_model_caching/>

- 12.cache_chat_model_response_inmemory.py: 'InMemoryCache'를 사용하여 캐시된 데이터를 반환하기
- 13.cache_chat_model_response_sqlite.py: 'SQLiteCache'를 사용하여 캐시된 데이터를 반환하기

### How to get log probabilities

<https://python.langchain.com/v0.2/docs/how_to/logprobs/>

- 14.logprobs.py: OpenAI - 'logprobs=True' - log probabilities 반환하기

### How to create a custom chat model class

<https://python.langchain.com/v0.2/docs/how_to/custom_chat_model/>

사용자 정의 chat model 구현 하기 - 입력의 n 번째까지 반환하기

- 15.custom_chat_model.py: 'BaseChatModel' 상속하여 사용자 정의 chat model 구현하기

### How to stream chat model responses

<https://python.langchain.com/v0.2/docs/how_to/chat_streaming/>

- 16.stream_chat_model_responses.py: 'stream'을 사용하여 chat model의 응답을 스트리밍 하기

### How to track token usage in ChatModels

<https://python.langchain.com/v0.2/docs/how_to/chat_token_usage_tracking/>

- Using LangSmith: <https://docs.smith.langchain.com/>
- 17.use_usage_metadata.py: 'usage_metadata' - token 사용량
- 18.use_callbacks.py: 'callbacks' - 'get_openai_callback' - token 사용량

### Response metadata

<https://python.langchain.com/v0.2/docs/how_to/response_metadata/>

OpenAI만 확인 - 나머지는 필요 시 확인

- 19.response_metadata.py: 'response_metadata' - metadata 확인

### How to init any model in one line

<https://python.langchain.com/v0.2/docs/how_to/chat_models_universal_init/>

- 20.init_chat_model.py: 'init_chat_model' - 특정 모델을 초기화 하기

### How to use a model to call tools

<https://python.langchain.com/v0.2/docs/how_to/tool_calling/>

`### How to use a model to call tools`와 동일

### How to stream tool calls

<https://python.langchain.com/v0.2/docs/how_to/tool_streaming/>

- 21.stream_tool_calls.py: tool 호출을 스트리밍 하기

### How to use few-shot prompting with tool calling

<https://python.langchain.com/v0.2/docs/how_to/tools_few_shot/>

- 22.few_shot_tool_calls.py: few-shot tool 호출하기


### How to bind model-specific tools

<https://python.langchain.com/v0.2/docs/how_to/tools_model_specific/>

- 23.bind_model_specific_tools.py: 모델에 tools 바인딩 하기 - OpenAI

### How to force tool calling behavior

<https://python.langchain.com/v0.2/docs/how_to/tool_choice/>

- 24.force_tool_calling_behavior.py: 'tool_choice="Multiply"' - tool 호출 강제하기

### How to init any model in one line

`### How to init any model in one line`와 동일
