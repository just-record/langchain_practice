# pip install --upgrade --quiet langchain-core
from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

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


### 신중한 스키마 정의
class Classification(BaseModel):
    sentiment: str = Field(..., enum=["happy", "neutral", "sad"])
    aggressiveness: int = Field(
        ...,
        description="describes how aggressive the statement is, the higher the number the more aggressive",
        enum=[1, 2, 3, 4, 5],
    )
    language: str = Field(
        ..., enum=["spanish", "english", "french", "german", "italian"]
    )
    
    
tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""
)

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(
    Classification
)    


##################################################################################
### 1. 예제 1
print('1.', '-' * 50)
##################################################################################
inp = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"
prompt = tagging_prompt.invoke({"input": inp})
rprint(llm.invoke(prompt))
# 1. --------------------------------------------------
# Classification(sentiment='happy', aggressiveness=1, language='spanish')


##################################################################################
### 2. 예제 2
print('2.', '-' * 50)
##################################################################################
inp = "Estoy muy enojado con vos! Te voy a dar tu merecido!"
prompt = tagging_prompt.invoke({"input": inp})
rprint(llm.invoke(prompt))
# 2. --------------------------------------------------
# Classification(sentiment='sad', aggressiveness=5, language='spanish')


##################################################################################
### 3. 예제 3
print('3.', '-' * 50)
##################################################################################
inp = "Weather is ok here, I can go outside without much more than a coat"
prompt = tagging_prompt.invoke({"input": inp})
rprint(llm.invoke(prompt))
# 3. --------------------------------------------------
# Classification(sentiment='happy', aggressiveness=1, language='english')