from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from typing import Optional, Union
from typing_extensions import Annotated, TypedDict
# from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# llm = ChatOpenAI(model="gpt-4o-mini")
### gpt-4o-mini는 제대로 된 결과가 출력되지 않음 ###
# {'setup': "Why,,didn't,non,of,Mr,WhISKY'S,co,work,for,him?", 'punchline': "CATS,don't,work,for,ANYBODY!"}
llm = ChatOpenAI(model="gpt-4o")

##################################################################################
### 1. json mode
print('1.', '-' * 50)
##################################################################################

structured_llm = llm.with_structured_output(None, method="json_mode")

results = structured_llm.invoke(
    "Tell me a joke about cats, respond in JSON with `setup` and `punchline` keys"
)
rprint(results)
# 1. --------------------------------------------------
# {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'Because it wanted to keep an eye on the mouse!'}