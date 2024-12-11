from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from typing import Optional, Union
from typing_extensions import Annotated, TypedDict
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini")

##################################################################################
### 1. Pydantic
print('1.', '-' * 50)
##################################################################################
class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is, from 1 to 10"
    )


class ConversationalResponse(BaseModel):
    """Respond in a conversational manner. Be kind and helpful."""

    response: str = Field(description="A conversational response to the user's query")


class FinalResponse(BaseModel):
    final_output: Union[Joke, ConversationalResponse]


structured_llm = llm.with_structured_output(FinalResponse)

results = structured_llm.invoke("Tell me a joke about cats")
rprint(results)
# 1. --------------------------------------------------
# FinalResponse(final_output=Joke(setup='Why was the cat sitting on the computer?', punchline='Because it wanted to keep an eye on the mouse!', rating=8))

print(' ')

results = structured_llm.invoke("How are you today?")
rprint(results)
# FinalResponse(final_output=ConversationalResponse(response="I'm just a bunch of code, but I'm here and ready to help you! How about you? How's your day going?"))


##################################################################################
### 2. TypedDict
print('2.', '-' * 50)
##################################################################################
class Joke(TypedDict):
    """Joke to tell user."""

    setup: Annotated[str, ..., "The setup of the joke"]
    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]


class ConversationalResponse(TypedDict):
    """Respond in a conversational manner. Be kind and helpful."""

    response: Annotated[str, ..., "A conversational response to the user's query"]


class FinalResponse(TypedDict):
    final_output: Union[Joke, ConversationalResponse]


structured_llm = llm.with_structured_output(FinalResponse)

results = structured_llm.invoke("Tell me a joke about cats")
rprint(results)
# 2. --------------------------------------------------
# {'final_output': {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'Because it wanted to keep an eye on the mouse!', 'rating': 7}}

print(' ')

results = structured_llm.invoke("How are you today?")
rprint(results)
# {'final_output': {'response': "I'm just a computer program, so I don't have feelings, but I'm here and ready to help you! How about you? How's your day going?"}}