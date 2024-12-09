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

events = []
async def stream_events():
    async for event in chain.astream_events({"question": question}, version="v2"):
        events.append(event)        

import asyncio
asyncio.run(stream_events())        

print(events[:3])
print('-' * 50)
print(events[-2:])

# on_chain_start -> on_prompt_start -> on_prompt_end -> ... -> on_parser_end -> on_chain_end

