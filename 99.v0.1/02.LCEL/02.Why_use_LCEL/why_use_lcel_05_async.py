################################################################################
# without LCEL
################################################################################

# from typing import List

# import openai

# prompt_template = "Tell me a short joke about {topic}"
# # client = openai.OpenAI()
# async_client = openai.AsyncOpenAI()

# async def acall_chat_model(messages: List[dict]) -> str:
#     response = await async_client.chat.completions.create(
#         model="gpt-3.5-turbo", 
#         messages=messages,
#     )
#     return response.choices[0].message.content

# async def ainvoke_chain(topic: str) -> str:
#     prompt_value = prompt_template.format(topic=topic)
#     messages = [{"role": "user", "content": prompt_value}]
#     return await acall_chat_model(messages)

# # await ainvoke_chain("ice cream")
# import asyncio

# async def main():
#     result = await ainvoke_chain("ice cream")
#     print(result)

# if __name__ == "__main__":
#     asyncio.run(main())
   
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

# print(chain.ainvoke("ice cream"))

import asyncio

async def main():
    result = await chain.ainvoke("ice cream")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())