from dotenv import load_dotenv
load_dotenv()

from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import chain


def reverse_word(word: str):
    return word[::-1]


reverse_word = RunnableLambda(reverse_word)


@chain
async def reverse_and_double(word: str):
    return await reverse_word.ainvoke(word) * 2


### @chain 쓰면 아래 코드가 필요 없음
# reverse_and_double = RunnableLambda(reverse_and_double)


async def main():
    async for event in reverse_and_double.astream("1234"):
        print(event)

import asyncio
asyncio.run(main())        
