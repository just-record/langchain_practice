from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

# llm = ChatAnthropic(
#     model="claude-3-haiku-20240307", temperature=0
# ).configurable_alternatives(
#     # This gives this field an id
#     # When configuring the end runnable, we can then use this id to configure this field
#     ConfigurableField(id="llm"),
#     # This sets a default_key.
#     # If we specify this key, the default LLM (ChatAnthropic initialized above) will be used
#     default_key="anthropic",
#     # This adds a new option, with name `openai` that is equal to `ChatOpenAI()`
#     openai=ChatOpenAI(),
#     # This adds a new option, with name `gpt4` that is equal to `ChatOpenAI(model="gpt-4")`
#     gpt4omini=ChatOpenAI(model="gpt-4o-mini"),
#     # You can add more configuration options here
# )

llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0
).configurable_alternatives(
    ConfigurableField(id="llm"),
    default_key="openai-gpt-4o-mini",
    openai=ChatOpenAI(),
    gpt4=ChatOpenAI(model="gpt-4"),
)
prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm

##################################################################################
### 1. 초기 설정 값 사용
print('1.', '-' * 50)
##################################################################################
# By default it will call Anthropic
results = chain.invoke({"topic": "bears"})
rprint(results)
# 1. --------------------------------------------------
# AIMessage(
#     content='Why do bears have hairy coats?\n\nBecause they look silly in sweaters!',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 15,
#             'prompt_tokens': 13,
#             'total_tokens': 28,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_0aa8d3e20b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-9572e3f6-ba49-4ac3-8cd0-cf0a19a71d0e-0',
#     usage_metadata={'input_tokens': 13, 'output_tokens': 15, 'total_tokens': 28, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


##################################################################################
### 2. llm 변경
print('2.', '-' * 50)
##################################################################################
# We can use `.with_config(configurable={"llm": "openai"})` to specify an llm to use
results = chain.with_config(configurable={"llm": "openai"}).invoke({"topic": "bears"})
rprint(results)
# 2. --------------------------------------------------
# AIMessage(
#     content="Why don't bears wear shoes?\n\nBecause they have bear feet!",
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 14,
#             'prompt_tokens': 13,
#             'total_tokens': 27,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-3.5-turbo-0125',
#         'system_fingerprint': None,
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-ee371fb7-959c-43df-bb7c-5f7621cce8c5-0',
#     usage_metadata={'input_tokens': 13, 'output_tokens': 14, 'total_tokens': 27, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


##################################################################################
### 3. llm 초기 값으로 되돌리기
print('3.', '-' * 50)
##################################################################################
# If we use the `default_key` then it uses the default
results = chain.with_config(configurable={"llm": "openai-gpt-4o-mini"}).invoke({"topic": "bears"})
rprint(results)
# AIMessage(
#     content='Why do bears have hairy coats?\n\nBecause they look silly in sweaters!',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 15,
#             'prompt_tokens': 13,
#             'total_tokens': 28,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_0aa8d3e20b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-180b55d8-b970-4e7b-8e84-9a12e94e8932-0',
#     usage_metadata={'input_tokens': 13, 'output_tokens': 15, 'total_tokens': 28, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )




##################################################################################
### 4. Prompt 스위칭 하기
print('4.', '-' * 50)
##################################################################################
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = PromptTemplate.from_template(
    "Tell me a joke about {topic}"
).configurable_alternatives(
    # This gives this field an id
    # When configuring the end runnable, we can then use this id to configure this field
    ConfigurableField(id="prompt"),
    # This sets a default_key.
    # If we specify this key, the default prompt (asking for a joke, as initialized above) will be used
    default_key="joke",
    # This adds a new option, with name `poem`
    poem=PromptTemplate.from_template("Write a short poem about {topic}"),
    # You can add more configuration options here
)
chain = prompt | llm

# By default it will write a joke
results = chain.invoke({"topic": "bears"})
rprint(results)
# 4. --------------------------------------------------
# AIMessage(
#     content='Why do bears have hairy coats?\n\nBecause they look silly in sweaters!',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 15,
#             'prompt_tokens': 13,
#             'total_tokens': 28,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_d02d531b47',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-70d7fe5d-ff2f-4fc8-807c-182aac2576ca-0',
#     usage_metadata={'input_tokens': 13, 'output_tokens': 15, 'total_tokens': 28, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )

print(' ')
# We can configure it write a poem
results = chain.with_config(configurable={"prompt": "poem"}).invoke({"topic": "bears"})
rprint(results)
# AIMessage(
#     content="In the forest deep where shadows play,  \nBears roam freely, night and day.  \nWith fur like dusk and eyes like stars,  \nThey wander through the woods, near and far.  \n\nGentle giants, strong and wise,  \nThey 
# dance beneath the sprawling skies.  \nIn rivers cool, they catch their feast,  \nNature's power, beauty unleashed.  \n\nWhen winter whispers, they find their den,  \nIn dreams of spring, they’ll roam again.  \nMajestic bears, 
# both fierce and grand,  \nGuardians of the wild, they roam the land.  ",
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 119,
#             'prompt_tokens': 13,
#             'total_tokens': 132,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_0aa8d3e20b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-4fd444ed-51ce-4f2c-b729-bb6d78f4df6b-0',
#     usage_metadata={'input_tokens': 13, 'output_tokens': 119, 'total_tokens': 132, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


##################################################################################
### 5. Prompt와 LLMs 스위칭 하기
print('5.', '-' * 50)
##################################################################################
llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0
).configurable_alternatives(
    ConfigurableField(id="llm"),
    default_key="openai-gpt-4o-mini",
    openai=ChatOpenAI(),
    gpt4=ChatOpenAI(model="gpt-4"),
)

prompt = PromptTemplate.from_template(
    "Tell me a joke about {topic}"
).configurable_alternatives(
    ConfigurableField(id="prompt"),
    default_key="joke",
     poem=PromptTemplate.from_template("Write a short poem about {topic}"),
 )


chain = prompt | llm

# We can configure it write a poem with OpenAI
results = chain.with_config(configurable={"prompt": "poem", "llm": "openai"}).invoke(
    {"topic": "bears"}
)
rprint(results)
# 5. --------------------------------------------------
# AIMessage(
#     content="In the forest deep and dark they roam,\nBears with fur of brown and black,\nStrong and fierce, yet gentle too,\nIn their world they never lack.\n\nThey fish in streams and hunt for food,\nGathering berries in the 
# sun,\nMajestic creatures of the wild,\nTheir journey has just begun.\n\nWith paws that crush and claws that tear,\nThey rule their land with pride,\nBut deep inside their hearts are kind,\nAnd in their eyes, no lies 
# reside.\n\nSo let us honor these mighty beasts,\nFor they are nature's crown,\nBears in all their glory,\nIn the wild, forever renowned.",
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 127,
#             'prompt_tokens': 13,
#             'total_tokens': 140,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-3.5-turbo-0125',
#         'system_fingerprint': None,
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-bc808eba-3196-48df-9ade-d42cfc209b47-0',
#     usage_metadata={'input_tokens': 13, 'output_tokens': 127, 'total_tokens': 140, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )

print(' ')
# We can always just configure only one if we want
results = chain.with_config(configurable={"llm": "openai"}).invoke({"topic": "bears"})
rprint(results)
# AIMessage(
#     content="Why did the bear break up with his girlfriend? Because he couldn't bear the relationship any longer!",
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 21,
#             'prompt_tokens': 13,
#             'total_tokens': 34,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-3.5-turbo-0125',
#         'system_fingerprint': None,
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-953f97ea-9161-481f-a675-e5bef3dc69d1-0',
#     usage_metadata={'input_tokens': 13, 'output_tokens': 21, 'total_tokens': 34, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


##################################################################################
### 6. 설정 저장하기
print('6.', '-' * 50)
##################################################################################
openai_joke = chain.with_config(configurable={"llm": "openai"})

results = openai_joke.invoke({"topic": "bears"})
rprint(results)
# 6. --------------------------------------------------
# AIMessage(
#     content="Why did the bear break up with his girlfriend? \n\nBecause he couldn't bear the relationship anymore!",
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 21,
#             'prompt_tokens': 13,
#             'total_tokens': 34,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-3.5-turbo-0125',
#         'system_fingerprint': None,
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-92302c39-0395-4349-a0f6-644f20655c57-0',
#     usage_metadata={'input_tokens': 13, 'output_tokens': 21, 'total_tokens': 34, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )