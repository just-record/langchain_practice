from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

async def _extract_country_names_streaming(input_stream):
    """A function that operates on input streams."""
    country_names_so_far = set()

    async for input in input_stream:
        if not isinstance(input, dict):
            continue

        if "countries" not in input:
            continue

        countries = input["countries"]

        if not isinstance(countries, list):
            continue

        for country in countries:
            name = country.get("name")
            if not name:
                continue
            if name not in country_names_so_far:
                yield name
                country_names_so_far.add(name)

model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("{question}")
chain = prompt | model | JsonOutputParser() | _extract_country_names_streaming

question = "output a list of the countries france, spain and japan and their populations in JSON format. "
'Use a dict with an outer key of "countries" which contains a list of countries. '
"Each country should have the key `name` and `population`"

async def answer_stream():
    async for chunk in chain.astream({"question": question}):
        print(chunk, end="|", flush=True)
        # print(chunk, flush=True)

import asyncio
asyncio.run(answer_stream())        
