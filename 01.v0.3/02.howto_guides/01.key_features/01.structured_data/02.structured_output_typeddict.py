from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from typing import Optional
from typing_extensions import Annotated, TypedDict

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini")

##################################################################################
### 1. TypedDict으로 출력을 구조화 하기
print('1.', '-' * 50)
##################################################################################


# TypedDict
class Joke(TypedDict):
    """Joke to tell user."""

    setup: Annotated[str, ..., "The setup of the joke"]

    # Alternatively, we could have specified setup as:

    # setup: str                    # no default, no description
    # setup: Annotated[str, ...]    # no default, no description
    # setup: Annotated[str, "foo"]  # default, no description

    punchline: Annotated[str, ..., "The punchline of the joke"]
    ### `...`는 pass 느낌. 빈칸으로 두지 않고 Ellipsis(`...`)를 사용하여 가독성을 높이고 의도를 명확히 할 수 있다. ###
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]


structured_llm = llm.with_structured_output(Joke)

results = structured_llm.invoke("Tell me a joke about cats")
rprint(results)
# 1. --------------------------------------------------
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'Because it wanted to keep an eye on the mouse!', 'rating': 7}


##################################################################################
### 2. JSON Schema dict로 출력을 구조화 하기 - import X, classes X
print('2.', '-' * 50)
##################################################################################
json_schema = {
    "title": "joke",
    "description": "Joke to tell user.",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "The setup of the joke",
        },
        "punchline": {
            "type": "string",
            "description": "The punchline to the joke",
        },
        "rating": {
            "type": "integer",
            "description": "How funny the joke is, from 1 to 10",
            "default": None,
        },
    },
    "required": ["setup", "punchline"],
}
structured_llm = llm.with_structured_output(json_schema)

results = structured_llm.invoke("Tell me a joke about cats")
rprint(results)
# 2. --------------------------------------------------
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'Because it wanted to keep an eye on the mouse!', 'rating': 8}