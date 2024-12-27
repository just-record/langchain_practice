from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from langchain_core.messages import (
    AIMessageChunk,
    FunctionMessageChunk,
    HumanMessageChunk,
    SystemMessageChunk,
    ToolMessageChunk,
)


from typing import Any, Dict, Iterator, List, Optional

from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
)
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
)
from langchain_core.messages.ai import UsageMetadata
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from pydantic import Field


class ChatParrotLink(BaseChatModel):
    """A custom chat model that echoes the first `parrot_buffer_length` characters
    of the input.

    When contributing an implementation to LangChain, carefully document
    the model including the initialization parameters, include
    an example of how to initialize the model and include any relevant
    links to the underlying models documentation or API.

    Example:

        .. code-block:: python

            model = ChatParrotLink(parrot_buffer_length=2, model="bird-brain-001")
            result = model.invoke([HumanMessage(content="hello")])
            result = model.batch([[HumanMessage(content="hello")],
                                 [HumanMessage(content="world")]])
    """

    model_name: str = Field(alias="model")
    """The name of the model"""
    parrot_buffer_length: int
    """The number of characters from the last message of the prompt to be echoed."""
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    stop: Optional[List[str]] = None
    max_retries: int = 2

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Override the _generate method to implement the chat model logic.

        This can be a call to an API, a call to a local model, or any other
        implementation that generates a response to the input prompt.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.
            run_manager: A run manager with callbacks for the LLM.
        """
        # Replace this with actual logic to generate a response from a list
        # of messages.
        last_message = messages[-1]
        tokens = last_message.content[: self.parrot_buffer_length]
        ct_input_tokens = sum(len(message.content) for message in messages)
        ct_output_tokens = len(tokens)
        message = AIMessage(
            content=tokens,
            additional_kwargs={},  # Used to add additional payload to the message
            response_metadata={  # Use for response metadata
                "time_in_seconds": 3,
            },
            usage_metadata={
                "input_tokens": ct_input_tokens,
                "output_tokens": ct_output_tokens,
                "total_tokens": ct_input_tokens + ct_output_tokens,
            },
        )
        ##

        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """Stream the output of the model.

        This method should be implemented if the model can generate output
        in a streaming fashion. If the model does not support streaming,
        do not implement it. In that case streaming requests will be automatically
        handled by the _generate method.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.
            run_manager: A run manager with callbacks for the LLM.
        """
        last_message = messages[-1]
        tokens = str(last_message.content[: self.parrot_buffer_length])
        ct_input_tokens = sum(len(message.content) for message in messages)

        for token in tokens:
            usage_metadata = UsageMetadata(
                {
                    "input_tokens": ct_input_tokens,
                    "output_tokens": 1,
                    "total_tokens": ct_input_tokens + 1,
                }
            )
            ct_input_tokens = 0
            chunk = ChatGenerationChunk(
                message=AIMessageChunk(content=token, usage_metadata=usage_metadata)
            )

            if run_manager:
                # This is optional in newer versions of LangChain
                # The on_llm_new_token will be called automatically
                run_manager.on_llm_new_token(token, chunk=chunk)

            yield chunk

        # Let's add some other information (e.g., response metadata)
        chunk = ChatGenerationChunk(
            message=AIMessageChunk(content="", response_metadata={"time_in_sec": 3})
        )
        if run_manager:
            # This is optional in newer versions of LangChain
            # The on_llm_new_token will be called automatically
            run_manager.on_llm_new_token(token, chunk=chunk)
        yield chunk

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model."""
        return "echoing-chat-model-advanced"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters.

        This information is used by the LangChain callback system, which
        is used for tracing purposes make it possible to monitor LLMs.
        """
        return {
            # The model name allows users to specify custom token counting
            # rules in LLM monitoring applications (e.g., in LangSmith users
            # can provide per token pricing for their model and monitor
            # costs for the given LLM.)
            "model_name": self.model_name,
        }
        
        
from rich import print as rprint

model = ChatParrotLink(parrot_buffer_length=3, model="my_custom_model")
#################################################################################
### 1. Test - invoke
print('1.', '-' * 50)
##################################################################################
results = model.invoke(
    [
        HumanMessage(content="hello!"),
        AIMessage(content="Hi there human!"),
        HumanMessage(content="Meow!"),
    ]
)        
rprint(results)
# 1. --------------------------------------------------
# AIMessage(content='Meo', additional_kwargs={}, response_metadata={'time_in_seconds': 3}, id='run-b308bae0-f471-4a85-8417-1f9268109b5c-0', usage_metadata={'input_tokens': 26, 'output_tokens': 3, 'total_tokens': 29})


#################################################################################
### 2. Test - invoke - string
print('2.', '-' * 50)
##################################################################################
print(model.invoke("hello"))
# 2. --------------------------------------------------
# content='hel' additional_kwargs={} response_metadata={'time_in_seconds': 3} id='run-1e3569b6-0cda-4e45-850c-07f50d4fa95e-0' usage_metadata={'input_tokens': 5, 'output_tokens': 3, 'total_tokens': 8}


#################################################################################
### 3. Test - batch
print('3.', '-' * 50)
##################################################################################
print(model.batch(["hello", "goodbye"]))
# 3. --------------------------------------------------
# [AIMessage(content='hel', additional_kwargs={}, response_metadata={'time_in_seconds': 3}, id='run-1376955d-c833-4510-bc99-a40e8e1bb704-0', usage_metadata={'input_tokens': 5, 'output_tokens': 3, 'total_tokens': 8}), AIMessage(content='goo', additional_kwargs={}, response_metadata={'time_in_seconds': 3}, id='run-0b01cfc3-71f9-4ece-b1dc-29862934b0ce-0', usage_metadata={'input_tokens': 7, 'output_tokens': 3, 'total_tokens': 10})]


#################################################################################
### 4. Test - stream
print('4.', '-' * 50)
##################################################################################
for chunk in model.stream("cat"):
    print(chunk.content, end="|")
# 4. --------------------------------------------------
# c|a|t||    
    
async def astream_func():
    async for chunk in model.astream("cat"):
        print(chunk.content, end="|")    
    
async def astream_events_func():
    async for event in model.astream_events("cat", version="v1"):
        print(event)    
        
import asyncio

#################################################################################
### 5. Test - astream
print('5.', '-' * 50)
##################################################################################
asyncio.run(astream_func())
# 5. --------------------------------------------------
# c|a|t||


#################################################################################
### 6. Test - astream_events
print('6.', '-' * 50)
##################################################################################
asyncio.run(astream_events_func())    
# 6. --------------------------------------------------
# {'event': 'on_chat_model_start', 'run_id': '28ea2184-e550-4e0b-a8bd-f6073a0f6e7d', 'name': 'ChatParrotLink', 'tags': [], 'metadata': {}, 'data': {'input': 'cat'}, 'parent_ids': []}
# {'event': 'on_chat_model_stream', 'run_id': '28ea2184-e550-4e0b-a8bd-f6073a0f6e7d', 'tags': [], 'metadata': {}, 'name': 'ChatParrotLink', 'data': {'chunk': AIMessageChunk(content='c', additional_kwargs={}, response_metadata={}, id='run-28ea2184-e550-4e0b-a8bd-f6073a0f6e7d', usage_metadata={'input_tokens': 3, 'output_tokens': 1, 'total_tokens': 4})}, 'parent_ids': []}
# {'event': 'on_chat_model_stream', 'run_id': '28ea2184-e550-4e0b-a8bd-f6073a0f6e7d', 'tags': [], 'metadata': {}, 'name': 'ChatParrotLink', 'data': {'chunk': AIMessageChunk(content='a', additional_kwargs={}, response_metadata={}, id='run-28ea2184-e550-4e0b-a8bd-f6073a0f6e7d', usage_metadata={'input_tokens': 0, 'output_tokens': 1, 'total_tokens': 1})}, 'parent_ids': []}
# {'event': 'on_chat_model_stream', 'run_id': '28ea2184-e550-4e0b-a8bd-f6073a0f6e7d', 'tags': [], 'metadata': {}, 'name': 'ChatParrotLink', 'data': {'chunk': AIMessageChunk(content='t', additional_kwargs={}, response_metadata={}, id='run-28ea2184-e550-4e0b-a8bd-f6073a0f6e7d', usage_metadata={'input_tokens': 0, 'output_tokens': 1, 'total_tokens': 1})}, 'parent_ids': []}
# {'event': 'on_chat_model_stream', 'run_id': '28ea2184-e550-4e0b-a8bd-f6073a0f6e7d', 'tags': [], 'metadata': {}, 'name': 'ChatParrotLink', 'data': {'chunk': AIMessageChunk(content='', additional_kwargs={}, response_metadata={'time_in_sec': 3}, id='run-28ea2184-e550-4e0b-a8bd-f6073a0f6e7d')}, 'parent_ids': []}
# {'event': 'on_chat_model_end', 'name': 'ChatParrotLink', 'run_id': '28ea2184-e550-4e0b-a8bd-f6073a0f6e7d', 'tags': [], 'metadata': {}, 'data': {'output': AIMessageChunk(content='cat', additional_kwargs={}, response_metadata={'time_in_sec': 3}, id='run-28ea2184-e550-4e0b-a8bd-f6073a0f6e7d', usage_metadata={'input_tokens': 3, 'output_tokens': 3, 'total_tokens': 6})}, 'parent_ids': []}    