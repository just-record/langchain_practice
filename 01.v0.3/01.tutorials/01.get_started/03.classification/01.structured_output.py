# pip install --upgrade --quiet langchain-core
from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(model="gpt-4o-mini")

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""
)


class Classification(BaseModel):
    sentiment: str = Field(description="The sentiment of the text")
    aggressiveness: int = Field(
        description="How aggressive the text is on a scale from 1 to 10"
    )
    language: str = Field(description="The language the text is written in")


##################################################################################
### 1. with_structured_output으로 출력 구조 정의하기
print('1.', '-' * 50)
##################################################################################
# LLM
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(
    Classification
)

inp = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"
prompt = tagging_prompt.invoke({"input": inp})
rprint(prompt)
# ChatPromptValue(
#     messages=[
#         HumanMessage(
#             content="\nExtract the desired information from the following passage.\n\nOnly extract the properties mentioned in the 'Classification' function.\n\nPassage:\nEstoy
# increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!\n",
#             additional_kwargs={},
#             response_metadata={}
#         )
#     ]
# )
print(' ')
response = llm.invoke(prompt)
rprint(response)
# Classification(sentiment='positive', aggressiveness=1, language='Spanish')


##################################################################################
### 2. `.dict()`를 사용하여 출력 바로 가져오기
print('2.', '-' * 50)
##################################################################################
inp = "Estoy muy enojado con vos! Te voy a dar tu merecido!"
prompt = tagging_prompt.invoke({"input": inp})
response = llm.invoke(prompt)
rprint(response.dict())
# 2. --------------------------------------------------
# {'sentiment': 'enojado', 'aggressiveness': 8, 'language': 'es'}