from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

##################################################################################
### 1. LCEL(LangChain Expression Language)
print('1.', '-' * 50)
##################################################################################
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
parser = StrOutputParser()
chain = prompt | model | parser

import asyncio

async def astream_func():
    async for chunk in chain.astream({"topic": "parrot"}):
        print(chunk, end="|", flush=True)
        
asyncio.run(astream_func())
# 1. --------------------------------------------------
# |Why| did| the| par|rot| wear| a| rain|coat|?

# |Because| it| wanted| to| be| a| poly|uns|aturated|!||
