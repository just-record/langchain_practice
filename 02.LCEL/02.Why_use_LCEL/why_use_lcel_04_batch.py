################################################################################
# without LCEL
################################################################################

# from typing import List

# import openai
# from concurrent.futures import ThreadPoolExecutor

# prompt_template = "Tell me a short joke about {topic}"
# client = openai.OpenAI()

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

# def batch_chain(topics: list) -> list:
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         return list(executor.map(invoke_chain, topics))


# print(batch_chain(["ice cream", "spaghetti", "dumplings"]))

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
print(chain.batch(["ice cream", "spaghetti", "dumplings"]))

