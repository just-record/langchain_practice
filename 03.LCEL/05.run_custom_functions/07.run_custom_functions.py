from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from typing import AsyncIterator, List


async def asplit_into_list(
    input: AsyncIterator[str],
) -> AsyncIterator[List[str]]:  # async def
    buffer = ""
    async for (
        chunk
    ) in input:  # `input` is a `async_generator` object, so use `async for`
        buffer += chunk
        while "," in buffer:
            comma_index = buffer.index(",")
            yield [buffer[:comma_index].strip()]
            buffer = buffer[comma_index + 1 :]
    yield [buffer.strip()]


prompt = ChatPromptTemplate.from_template(
    "Write a comma-separated list of 5 animals similar to: {animal}. Do not include numbers"
)

model = ChatOpenAI(model="gpt-3.5-turbo")

str_chain = prompt | model | StrOutputParser()

list_chain = str_chain | asplit_into_list

async def answer_stream():
    async for chunk in list_chain.astream({"animal": "bear"}):
        print(chunk, flush=True)

import asyncio
asyncio.run(answer_stream())
### 또는
# print(asyncio.run(list_chain.ainvoke({"animal": "bear"})))
