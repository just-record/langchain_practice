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
    

class ConversationalResponse(BaseModel):
    """Respond in a conversational manner. Be kind and helpful."""

    response: str = Field(description="A conversational response to the user's query")


class Response(BaseModel):
    output: Joke | ConversationalResponse


structured_llm = llm.with_structured_output(Response)

### 1. Joke
results = structured_llm.invoke("Tell me a joke about cats")
print(results)
# output=Joke(setup='Why was the cat sitting on the computer?', punchline='To keep an eye on the mouse!', rating=8)

### 2. 인사
print('-'*30)
results = structured_llm.invoke("How are you today?")
print(results)
# output=ConversationalResponse(response="I'm just a program, so I don't have feelings, but I'm here to help you with anything you need. How can I assist you today?")