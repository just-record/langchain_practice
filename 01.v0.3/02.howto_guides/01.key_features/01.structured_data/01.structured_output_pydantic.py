from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from typing import Optional
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini")

##################################################################################
### 1. Pydantic으로 출력을 구조화 하기
print('1.', '-' * 50)
##################################################################################
# Pydantic
class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is, from 1 to 10"
    )


structured_llm = llm.with_structured_output(Joke)

results = structured_llm.invoke("Tell me a joke about cats")
rprint(results)
# 1. --------------------------------------------------
# Joke(setup='Why was the cat sitting on the computer?', punchline='Because it wanted to keep an eye on the mouse!', rating=7)
print(' ')
print(results.setup)
print(results.punchline)
print(results.rating)
# Why was the cat sitting on the computer?
# Because it wanted to keep an eye on the mouse!
# 7