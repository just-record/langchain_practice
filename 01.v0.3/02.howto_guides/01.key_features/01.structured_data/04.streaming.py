from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from typing import Optional, Union
from typing_extensions import Annotated, TypedDict
# from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini")

##################################################################################
### 1. TypedDict
print('1.', '-' * 50)
##################################################################################
# TypedDict
class Joke(TypedDict):
    """Joke to tell user."""

    setup: Annotated[str, ..., "The setup of the joke"]
    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]


structured_llm = llm.with_structured_output(Joke)

for chunk in structured_llm.stream("Tell me a joke about cats"):
    print(chunk)
# 1. --------------------------------------------------
# {}
# {'setup': ''}
# {'setup': 'Why'}
# {'setup': 'Why did'}
# {'setup': 'Why did the'}
# {'setup': 'Why did the cat'}
# {'setup': 'Why did the cat sit'}
# {'setup': 'Why did the cat sit on'}
# {'setup': 'Why did the cat sit on the'}
# {'setup': 'Why did the cat sit on the computer'}
# {'setup': 'Why did the cat sit on the computer?'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': ''}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep an'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep an eye'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep an eye on'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep an eye on the'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep an eye on the mouse'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep an eye on the mouse!'}
# {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep an eye on the mouse!', 'rating': 8}    