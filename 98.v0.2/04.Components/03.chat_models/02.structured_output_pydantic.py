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


structured_llm = llm.with_structured_output(Joke)

results = structured_llm.invoke("Tell me a joke about cats")
print(results)
# setup='Why was the cat sitting on the computer?' punchline='To keep an eye on the mouse!' rating=8