from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
openai_response = llm.invoke("hello")
print(openai_response.usage_metadata)
# {'input_tokens': 8, 'output_tokens': 9, 'total_tokens': 17}

### 모델에 따라 다름
# print(f'OpenAI: {openai_response.response_metadata["token_usage"]}\n')
# print(f'Anthropic: {anthropic_response.response_metadata["usage"]}')


### streaming
print('-'*30)
aggregate = None
for chunk in llm.stream("hello", stream_options={"include_usage": True}):
    print(chunk)
    aggregate = chunk if aggregate is None else aggregate + chunk

print('-'*30)
print(f'aggregate.content: {aggregate.content}')
print(f'aggregate.usage_metadata: {aggregate.usage_metadata}')


### setting model_kwargs
print('-'*30)
from langchain_core.pydantic_v1 import BaseModel, Field


class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")


llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    model_kwargs={"stream_options": {"include_usage": True}},
)
# Under the hood, .with_structured_output binds tools to the
# chat model and appends a parser.
structured_llm = llm.with_structured_output(Joke)

async def chat_astream_events():
    async for event in structured_llm.astream_events("Tell me a joke", version="v2"):
        if event["event"] == "on_chat_model_end":
            print(f'Token usage: {event["data"]["output"].usage_metadata}\n')
        elif event["event"] == "on_chain_end":
            print(event["data"]["output"])
        else:
            pass


import asyncio
asyncio.run(chat_astream_events())
# Token usage: {'input_tokens': 72, 'output_tokens': 32, 'total_tokens': 104}

# setup="Why couldn't the bicycle stand up by itself?" punchline='Because it was two tired!'