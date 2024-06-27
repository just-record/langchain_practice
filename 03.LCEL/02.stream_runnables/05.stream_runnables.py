from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# A function that operates on finalized inputs
# rather than on an input_stream
def _extract_country_names(inputs):
    """A function that does not operates on input streams and breaks streaming."""
    if not isinstance(inputs, dict):
        return ""

    if "countries" not in inputs:
        return ""

    countries = inputs["countries"]

    if not isinstance(countries, list):
        return ""

    country_names = [
        country.get("name") for country in countries if isinstance(country, dict)
    ]
    return country_names

model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("{question}")
chain = prompt | model | JsonOutputParser() | _extract_country_names

question = "output a list of the countries france, spain and japan and their populations in JSON format. "
'Use a dict with an outer key of "countries" which contains a list of countries. '
"Each country should have the key `name` and `population`"

async def answer_stream():
    async for chunk in chain.astream({"question": question}):
        print(chunk, end="|", flush=True)
        # print(chunk, flush=True)

import asyncio
asyncio.run(answer_stream())        
