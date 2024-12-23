from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
joke_chain = ChatPromptTemplate.from_template("tell me a joke about {topic}") | model
poem_chain = (
    ChatPromptTemplate.from_template("write a 2-line poem about {topic}") | model
)

##################################################################################
### 1. 여러 Runnable을 병렬로 실행하고, 이러한 Runnable의 출력을 맵으로 반환
print('1.', '-' * 50)
##################################################################################

map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

results = map_chain.invoke({"topic": "bear"})
rprint(results)
# 1. --------------------------------------------------
# {
#     'joke': AIMessage(
#         content='Why did the bear bring a flashlight to the party? Because he heard it was going to be a "beary" good time!',
#         additional_kwargs={'refusal': None},
#         response_metadata={
#             'token_usage': {
#                 'completion_tokens': 28,
#                 'prompt_tokens': 13,
#                 'total_tokens': 41,
#                 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#                 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#             },
#             'model_name': 'gpt-3.5-turbo-0125',
#             'system_fingerprint': None,
#             'finish_reason': 'stop',
#             'logprobs': None
#         },
#         id='run-673dcfa4-adf6-4e5e-b031-e116472e06a0-0',
#         usage_metadata={'input_tokens': 13, 'output_tokens': 28, 'total_tokens': 41, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
#     ),
#     'poem': AIMessage(
#         content='In the dark forest, a bear roams free\nMajestic creature, wild and mighty',
#         additional_kwargs={'refusal': None},
#         response_metadata={
#             'token_usage': {
#                 'completion_tokens': 20,
#                 'prompt_tokens': 15,
#                 'total_tokens': 35,
#                 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#                 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#             },
#             'model_name': 'gpt-3.5-turbo-0125',
#             'system_fingerprint': None,
#             'finish_reason': 'stop',
#             'logprobs': None
#         },
#         id='run-419b396e-8548-4142-b34e-cc461c25eb35-0',
#         usage_metadata={'input_tokens': 15, 'output_tokens': 20, 'total_tokens': 35, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
#     )
# }


##################################################################################
### 2.  joke_chain, poem_chain 및 map_chain이 모두 비슷한 실행 시간. 
### 물론 2개 다 병렬로 실행되어도 비슷한 실행 시간
print('2.', '-' * 50)
##################################################################################
import time

# 함수의 실행 시간 측정ㄹ
def measure_execution_time(func):
    total_time = 0
    
    start_time = time.perf_counter()
    func()
    end_time = time.perf_counter()
    total_time += (end_time - start_time)
    
    print(f"{total_time:.6f} seconds")


def run_joke_chain():
    return joke_chain.invoke({"topic": "bear"})


def run_poem_chain():
    return poem_chain.invoke({"topic": "bear"})


def run_map_chain():
    return map_chain.invoke({"topic": "bear"})


measure_execution_time(run_joke_chain)
# 2. --------------------------------------------------
# 0.672079 seconds

measure_execution_time(run_poem_chain)
# 0.666363 seconds


measure_execution_time(run_map_chain)
# 0.694219 seconds


