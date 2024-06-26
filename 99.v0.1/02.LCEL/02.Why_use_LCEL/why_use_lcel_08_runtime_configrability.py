################################################################################
# without LCEL
################################################################################

# from typing import List, Iterator

# import openai


# prompt_template = "Tell me a short joke about {topic}"
# client = openai.OpenAI()

# ############# chat_openai ##################

# def call_chat_model(messages: List[dict]) -> str:
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo", 
#         messages=messages,
#     )
#     return response.choices[0].message.content

# def invoke_chain(topic: str) -> str:
#     prompt_value = prompt_template.format(topic=topic)
#     messages = [{"role": "user", "content": prompt_value}]
#     return call_chat_model(messages)

# ############# openai ##################
# def call_llm(prompt_value: str) -> str:
#     response = client.completions.create(
#         model="gpt-3.5-turbo-instruct",
#         prompt=prompt_value,
#     )
#     return response.choices[0].text

# def invoke_llm_chain(topic: str) -> str:
#     prompt_value = prompt_template.format(topic=topic)
#     return call_llm(prompt_value)

# ############# anthropic ##################
# # import anthropic

# # anthropic_template = f"Human:\n\n{prompt_template}\n\nAssistant:"
# # anthropic_client = anthropic.Anthropic()

# # def call_anthropic(prompt_value: str) -> str:
# #     response = anthropic_client.completions.create(
# #         model="claude-2",
# #         prompt=prompt_value,
# #         max_tokens_to_sample=256,
# #     )
# #     return response.completion    

# # def invoke_anthropic_chain(topic: str) -> str:
# #     prompt_value = anthropic_template.format(topic=topic)
# #     return call_anthropic(prompt_value)

# # anthropicfmf 설치 하지 않아 위의 llm 모델을 사용
# def invoke_anthropic_chain(topic: str) -> str:
#     prompt_value = prompt_template.format(topic=topic)
#     return call_llm(prompt_value)


# def stream_chat_model(messages: List[dict]) -> Iterator[str]:
#     stream = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         stream=True,
#     )
#     for response in stream:
#         content = response.choices[0].delta.content
#         if content is not None:
#             yield content
        
# def stream_chain(topic: str) -> Iterator[str]:
#     prompt_value = prompt_template.format(topic=topic)
#     return stream_chat_model([{"role": "user", "content": prompt_value}])    

# # 동일 모델 사용
# def stream_llm_chain(topic: str) -> Iterator[str]:
#     prompt_value = prompt_template.format(topic=topic)
#     return stream_chat_model([{"role": "user", "content": prompt_value}])   

# # 동일 모델 사용
# def stream_anthropic_chain(topic: str) -> Iterator[str]:
#     prompt_value = prompt_template.format(topic=topic)
#     return stream_chat_model([{"role": "user", "content": prompt_value}])   


# ############# invoke_configurable_chain ##################

# def invoke_configurable_chain(
#     topic: str, 
#     *, 
#     model: str = "chat_openai"
# ) -> str:
#     if model == "chat_openai":
#         return invoke_chain(topic)
#     elif model == "openai":
#         return invoke_llm_chain(topic)
#     elif model == "anthropic":
#         return invoke_anthropic_chain(topic)
#     else:
#         raise ValueError(
#             f"Received invalid model '{model}'."
#             " Expected one of chat_openai, openai, anthropic"
#         )
    
# def stream_configurable_chain(
#     topic: str, 
#     *, 
#     model: str = "chat_openai"
# ) -> Iterator[str]:
#     if model == "chat_openai":
#         return stream_chain(topic)
#     elif model == "openai":
#         # Note we haven't implemented this yet.
#         return stream_llm_chain(topic)
#     elif model == "anthropic":
#         # Note we haven't implemented this yet
#         return stream_anthropic_chain(topic)
#     else:
#         raise ValueError(
#             f"Received invalid model '{model}'."
#             " Expected one of chat_openai, openai, anthropic"
#         )

# def batch_configurable_chain(
#     topics: List[str], 
#     *, 
#     model: str = "chat_openai"
# ) -> List[str]:
#     # You get the idea
#     ...

# async def abatch_configurable_chain(
#     topics: List[str], 
#     *, 
#     model: str = "chat_openai"
# ) -> List[str]:
#     ...

# invoke_configurable_chain("ice cream", model="openai")
# stream = stream_configurable_chain(
#     "ice_cream", 
#     model="anthropic"
# )
# for chunk in stream:
#     print(chunk, end="", flush=True)

# # batch_configurable_chain(["ice cream", "spaghetti", "dumplings"])
# # await ainvoke_configurable_chain("ice cream")
   
################################################################################
# with LCEL
################################################################################

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI

prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")

model = ChatOpenAI(model="gpt-3.5-turbo")
llm = OpenAI(model='gpt-3.5-turbo-instruct')
# 동일 모델 사용
anthropic = ChatOpenAI(model="gpt-3.5-turbo")

output_parser = StrOutputParser()

configurable_model = model.configurable_alternatives(
    ConfigurableField(id="model"), 
    default_key="chat_openai", 
    openai=llm,
    anthropic=anthropic,
)
configurable_chain = (
    {"topic": RunnablePassthrough()} 
    | prompt 
    | configurable_model 
    | output_parser
)

configurable_chain.invoke(
    "ice cream", 
    config={"model": "openai"}
)
stream = configurable_chain.stream(
    "ice cream", 
    config={"model": "anthropic"}
)
for chunk in stream:
    print(chunk, end="", flush=True)

print(configurable_chain.batch(["ice cream", "spaghetti", "dumplings"]))

# await configurable_chain.ainvoke("ice cream")