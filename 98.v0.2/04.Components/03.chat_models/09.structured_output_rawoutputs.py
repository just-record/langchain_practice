from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field


llm = ChatOpenAI(model="gpt-3.5-turbo")

class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: int | None = Field(description="How funny the joke is, from 1 to 10")


structured_llm = llm.with_structured_output(Joke, include_raw=True)

results = structured_llm.invoke(
    "Tell me a joke about cats, respond in JSON with `setup` and `punchline` keys"
)
print(results)
# {'raw': AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_oZE7K4nfNy5SwEKACPU0E5br', 'function': {'arguments': '{"setup":"Why was the cat sitting on the computer?","punchline":"To keep an eye on the mouse!"}', 'name': 'Joke'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 33, 'prompt_tokens': 107, 'total_tokens': 140}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None}, id='run-ba1dd972-be39-4a7a-be15-1f7f7ef6a23f-0', tool_calls=[{'name': 'Joke', 'args': {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'To keep an eye on the mouse!'}, 'id': 'call_oZE7K4nfNy5SwEKACPU0E5br'}], usage_metadata={'input_tokens': 107, 'output_tokens': 33, 'total_tokens': 140}), 'parsed': Joke(setup='Why was the cat sitting on the computer?', punchline='To keep an eye on the mouse!', rating=None), 'parsing_error': None}
