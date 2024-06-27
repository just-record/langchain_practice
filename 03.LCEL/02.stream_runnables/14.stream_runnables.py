from dotenv import load_dotenv
load_dotenv()

from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool


def reverse_word(word: str):
    return word[::-1]


reverse_word = RunnableLambda(reverse_word)

### bad_tool
# @tool
# def bad_tool(word: str):
#     """Custom tool that doesn't propagate callbacks."""
#     return reverse_word.invoke(word)


# async def stream_events():
#     async for event in bad_tool.astream_events("hello", version="v2"):
#         print(event)


### correct_tool        
@tool
def correct_tool(word: str, callbacks):
    """A tool that correctly propagates callbacks."""
    return reverse_word.invoke(word, {"callbacks": callbacks})


async def stream_events():
    async for event in correct_tool.astream_events("hello", version="v2"):
        print(event)

import asyncio
asyncio.run(stream_events())        
