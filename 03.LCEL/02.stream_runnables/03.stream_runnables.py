from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

model = ChatOpenAI(model="gpt-3.5-turbo-0125")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
parser = StrOutputParser()
chain = prompt | model | parser

chunks = []
async def answer_stream():
    async for chunk in chain.astream({"topic": "parrot"}):
    # async for chunk in (prompt | model | parser).astream({"topic": "parrot"}):
        print(chunk, end="|", flush=True)

import asyncio
asyncio.run(answer_stream())        
