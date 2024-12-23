from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI


##################################################################################
### 1. 실행 시간에 Chat model의 temperature Field를 설정 하기 
### configurable_fields()를 사용하여 ChatOpenAI의 temperature Field를 설정
### temperature는 실제 존재하는 필드
print('1.', '-' * 50)
##################################################################################
model = ChatOpenAI(temperature=0).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",   # 필수값
        name="LLM Temperature",
        description="The temperature of the LLM",
    )
)

results = model.invoke("pick a random number")
rprint(results)
# 1. --------------------------------------------------
# AIMessage(
#     content='27',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 2,
#             'prompt_tokens': 11,
#             'total_tokens': 13,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-3.5-turbo-0125',
#         'system_fingerprint': None,
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-ff58c16c-aefe-4ee2-8c21-0b803983da20-0',
#     usage_metadata={'input_tokens': 11, 'output_tokens': 2, 'total_tokens': 13, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


##################################################################################
### 2. with_config()로 값 설정하기
print('2.', '-' * 50)
##################################################################################
results = model.with_config(configurable={"llm_temperature": 0.9}).invoke("pick a random number")
rprint(results.content)

print(' ')
results = model.with_config(configurable={"llm_temperature": 0.0}).invoke("pick a random number")
rprint(results.content)
# 2. --------------------------------------------------
# 13
 
# 27


##################################################################################
### 3. 체인의 한 단계에 영향을 미치기
print('3.', '-' * 50)
##################################################################################
prompt = PromptTemplate.from_template("Pick a random number above {x}")
chain = prompt | model

results = chain.with_config(configurable={"llm_temperature": 0.9}).invoke({"x": 0})
rprint(results.content)

print(' ')
results = chain.invoke({"x": 0})
rprint(results.content)
# 3. --------------------------------------------------
# 75
 
# 27


##################################################################################
### 4. With HubRunnables - 프롬프트 스위칭 하기
print('4.', '-' * 50)
##################################################################################
from langchain.runnables.hub import HubRunnable

prompt = HubRunnable("rlm/rag-prompt").configurable_fields(
    owner_repo_commit=ConfigurableField(
        id="hub_commit",
        name="Hub Commit",
        description="The Hub commit to pull from",
    )
)

rprint(prompt.invoke({"question": "foo", "context": "bar"}))
# 4. --------------------------------------------------
# ChatPromptValue(
#     messages=[
#         HumanMessage(
#             content="You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences 
# maximum and keep the answer concise.\nQuestion: foo \nContext: bar \nAnswer:",
#             additional_kwargs={},
#             response_metadata={}
#         )
#     ]
# )

print(' ')
rprint(prompt.with_config(configurable={"hub_commit": "rlm/rag-prompt-llama"}).invoke(
    {"question": "foo", "context": "bar"}
))
# ChatPromptValue(
#     messages=[
#         HumanMessage(
#             content="[INST]<<SYS>> You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three 
# sentences maximum and keep the answer concise.<</SYS>> \nQuestion: foo \nContext: bar \nAnswer: [/INST]",
#             additional_kwargs={},
#             response_metadata={}
#         )
#     ]
# )