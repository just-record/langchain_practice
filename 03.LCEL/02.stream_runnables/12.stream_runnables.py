from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("{question}")
chain = prompt | model.with_config({"run_name": "model"}) | JsonOutputParser().with_config({"run_name": "my_parser"})
### By tags
# chain = (prompt | model | JsonOutputParser()).with_config({"tags": ["my_chain"]})

question = "output a list of the countries france, spain and japan and their populations in JSON format. "
'Use a dict with an outer key of "countries" which contains a list of countries. '
"Each country should have the key `name` and `population`"

events = []
async def stream_events():
    max_events = 0
    ### By name, By type, By tags
    async for event in chain.astream_events({"question": question}, version="v2", include_names=["my_parser"]):
    # async for event in chain.astream_events({"question": question}, version="v2", include_types=["chat_model"]):
    # async for event in chain.astream_events({"question": question}, version="v2", include_tags=["my_chain"]):
        print(event)
        max_events += 1
        if max_events > 10:
            # Truncate output
            print("...")
            break

import asyncio
asyncio.run(stream_events())        
