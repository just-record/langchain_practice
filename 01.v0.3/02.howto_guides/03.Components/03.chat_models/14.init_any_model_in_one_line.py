# 사용자가 애플리케이션을 구동할 모델 제공자와 모델을 지정
# 사용자 설정에 따라 다양한 채팅 모델을 초기화하는 로직
# init_chat_model() 헬퍼 메서드를 사용하면 임포트 경로나 클래스 이름을 신경 쓰지 않고도 여러 모델 통합을 쉽게 초기화

# pip install -qU langchain>=0.2.8 langchain-openai langchain-anthropic langchain-google-vertexai

from rich import print as rprint
from langchain.chat_models import init_chat_model

# Returns a langchain_openai.ChatOpenAI instance.
gpt_4o = init_chat_model("gpt-4o", model_provider="openai", temperature=0)
# Returns a langchain_anthropic.ChatAnthropic instance.
claude_opus = init_chat_model(
    "claude-3-opus-20240229", model_provider="anthropic", temperature=0
)

### 실습 생략: API KEY 필요
# Returns a langchain_google_vertexai.ChatVertexAI instance.
# gemini_15 = init_chat_model(
#     "gemini-1.5-pro", model_provider="google_vertexai", temperature=0
# )


#################################################################################
### 1. init_chat_model()을 사용하여 모델 초기화
print('1.', '-' * 50)
##################################################################################
# Since all model integrations implement the ChatModel interface, you can use them in the same way.
print("GPT-4o: " + gpt_4o.invoke("what's your name").content + "\n")
print("Claude Opus: " + claude_opus.invoke("what's your name").content + "\n")
# print("Gemini 1.5: " + gemini_15.invoke("what's your name").content + "\n")

# 1. --------------------------------------------------
# GPT-4o: I’m an AI language model created by OpenAI, and I don’t have a personal name. You can call me Assistant if you’d like!
# Claude Opus: My name is Claude. It's nice to meet you!


#################################################################################
### 2. configurable_fields() 메서드를 사용하여 실행 시에 모델 설정값 설정하기
print('2.', '-' * 50)
##################################################################################
configurable_model = init_chat_model(temperature=0)

rprint(configurable_model.invoke(
    "what's your name", config={"configurable": {"model": "gpt-4o"}}
))
# 2. --------------------------------------------------
# AIMessage(
#     content='I’m called ChatGPT. How can I assist you today?',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 14,
#             'prompt_tokens': 11,
#             'total_tokens': 25,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-2024-08-06',
#         'system_fingerprint': 'fp_d28bcae782',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-490b72d7-d685-4b36-90fd-10dc8180da60-0',
#     usage_metadata={'input_tokens': 11, 'output_tokens': 14, 'total_tokens': 25, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


print(' ')
rprint(configurable_model.invoke(
    "what's your name", config={"configurable": {"model": "claude-3-5-sonnet-20240620"}}
))
# AIMessage(
#     content="My name is Claude. It's nice to meet you!",
#     additional_kwargs={},
#     response_metadata={
#         'id': 'msg_0161ZStjUxw9qpfxkSsVgQbz',
#         'model': 'claude-3-5-sonnet-20240620',
#         'stop_reason': 'end_turn',
#         'stop_sequence': None,
#         'usage': {'input_tokens': 11, 'output_tokens': 15, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}
#     },
#     id='run-551c92c1-508f-4a16-8465-ae15e7438fe1-0',
#     usage_metadata={'input_tokens': 11, 'output_tokens': 15, 'total_tokens': 26, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}}
# )


#################################################################################
### 3. 기본값이 있는 구성 가능한 모델을 만들고, 
### 어떤 매개변수를 구성할 수 있는지 지정하고, 
### 구성 가능한 매개변수에 접두사를 추가
print('3.', '-' * 50)
##################################################################################
first_llm = init_chat_model(
    model="gpt-4o",
    temperature=0,
    configurable_fields=("model", "model_provider", "temperature", "max_tokens"),
    config_prefix="first",  # useful when you have a chain with multiple models
)

rprint(first_llm.invoke("what's your name"))
# 3. --------------------------------------------------
# AIMessage(
#     content='I’m called ChatGPT. How can I assist you today?',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 14,
#             'prompt_tokens': 11,
#             'total_tokens': 25,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-2024-08-06',
#         'system_fingerprint': 'fp_d28bcae782',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-e7a60764-1e48-4936-a4ff-09dc7a1170d9-0',
#     usage_metadata={'input_tokens': 11, 'output_tokens': 14, 'total_tokens': 25, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


print(' ')
rprint(first_llm.invoke(
    "what's your name",
    config={
        "configurable": {
            "first_model": "claude-3-5-sonnet-20240620",
            "first_temperature": 0.5,
            "first_max_tokens": 100,
        }
    },
))
# AIMessage(
#     content="My name is Claude. It's nice to meet you!",
#     additional_kwargs={},
#     response_metadata={
#         'id': 'msg_01M7ebrNi8dMCZiGo7pkXYh7',
#         'model': 'claude-3-5-sonnet-20240620',
#         'stop_reason': 'end_turn',
#         'stop_sequence': None,
#         'usage': {'input_tokens': 11, 'output_tokens': 15, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}
#     },
#     id='run-d8efe3c3-c623-443b-8d4a-302b29e2b602-0',
#     usage_metadata={'input_tokens': 11, 'output_tokens': 15, 'total_tokens': 26, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}}
# )