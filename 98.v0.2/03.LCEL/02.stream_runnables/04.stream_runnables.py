from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("{question}")
chain = prompt | model | JsonOutputParser()   # chain = prompt | model | StrOutputParser()

question = "output a list of the countries france, spain and japan and their populations in JSON format. "
'Use a dict with an outer key of "countries" which contains a list of countries. '
"Each country should have the key `name` and `population`"

async def answer_stream():
    async for chunk in chain.astream({"question": question}):
        # print(chunk, end="|", flush=True)
        print(chunk, flush=True)

import asyncio
asyncio.run(answer_stream())        

### stream을 사용하지 않을때
# results = chain.invoke({"question": question})
# print(results)
