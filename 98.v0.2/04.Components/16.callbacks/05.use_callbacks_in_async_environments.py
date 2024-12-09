from dotenv import load_dotenv
load_dotenv()

import asyncio
from typing import Any, Dict, List

from langchain_anthropic import ChatAnthropic
from langchain_core.callbacks import AsyncCallbackHandler, BaseCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_core.outputs import LLMResult


class MyCustomSyncHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"Sync handler being called in a `thread_pool_executor`: token: {token}")


class MyCustomAsyncHandler(AsyncCallbackHandler):
    """Async callback handler that can be used to handle callbacks from langchain."""

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when chain starts running."""
        print("zzzz....")
        await asyncio.sleep(0.3)
        class_name = serialized["name"]
        print("Hi! I just woke up. Your llm is starting")

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when chain ends running."""
        print("zzzz....")
        await asyncio.sleep(0.3)
        print("Hi! I just woke up. Your llm is ending")


# To enable streaming, we pass in `streaming=True` to the ChatModel constructor
# Additionally, we pass in a list with our custom handler
chat = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    max_tokens=25,
    streaming=True,
    callbacks=[MyCustomSyncHandler(), MyCustomAsyncHandler()],
)

async def main():
    chat = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        max_tokens=25,
        streaming=True,
        callbacks=[MyCustomSyncHandler(), MyCustomAsyncHandler()],
    )

    await chat.agenerate([[HumanMessage(content="Tell me a joke")]])

if __name__ == "__main__":
    asyncio.run(main())
# zzzz....
# Hi! I just woke up. Your llm is starting
# Sync handler being called in a `thread_pool_executor`: token: 
# Sync handler being called in a `thread_pool_executor`: token: Here
# Sync handler being called in a `thread_pool_executor`: token: 's a silly
# Sync handler being called in a `thread_pool_executor`: token:  joke for you:
# Sync handler being called in a `thread_pool_executor`: token: 

# Why can
# Sync handler being called in a `thread_pool_executor`: token: 't a bicycle
# Sync handler being called in a `thread_pool_executor`: token:  stand up by
# Sync handler being called in a `thread_pool_executor`: token:  itself?
# Sync handler being called in a `thread_pool_executor`: token: 
# Because it's two
# Sync handler being called in a `thread_pool_executor`: token: -
# Sync handler being called in a `thread_pool_executor`: token: 
# zzzz....
# Hi! I just woke up. Your llm is ending    