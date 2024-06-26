################################################################################
# without LCEL
################################################################################

# from typing import Iterator, List

# import openai

# prompt = "Tell me a short joke about {topic}"
# client = openai.OpenAI()


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
#     prompt_value = prompt.format(topic=topic)
#     return stream_chat_model([{"role": "user", "content": prompt_value}])


# for chunk in stream_chain("ice cream"):
#     print(chunk, end="", flush=True)

################################################################################
# with LCEL
################################################################################

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
model = ChatOpenAI(model="gpt-3.5-turbo")
chain = (
    {"topic": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# print(chain.invoke("ice cream"))
# # "Why did the ice cream go to therapy?\n\nBecause it had a rocky road!"

for chunk in chain.stream("ice cream"):
    print(chunk, end="", flush=True)

