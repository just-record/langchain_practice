from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

#################################################################################
### 1. 스트리밍 부수기
### '_extract_country_names'함수 사용 - 입력을 처리 하여 최종 결과 값을 return
print('1.', '-' * 50)
##################################################################################
from langchain_core.output_parsers import (
    JsonOutputParser,
)


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


chain = model | JsonOutputParser() | _extract_country_names

import asyncio

async def astream_func():
    async for chunk in chain.astream(
        "output a list of the countries france, spain and japan and their populations in JSON format. "
        'Use a dict with an outer key of "countries" which contains a list of countries. '
        "Each country should have the key `name` and `population`"
    ):
        print(chunk, end="|", flush=True)

asyncio.run(astream_func())
# 1. --------------------------------------------------
# ['France', 'Spain', 'Japan']|


#################################################################################
### 2. 스트리밍 수정하기 
### '_extract_country_names'을 yield를 사용 하여 generator로 변경
print('2.', '-' * 50)
##################################################################################
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


chain = model | JsonOutputParser() | _extract_country_names_streaming

async def astream_func():
    async for chunk in chain.astream(
        "output a list of the countries france, spain and japan and their populations in JSON format. "
        'Use a dict with an outer key of "countries" which contains a list of countries. '
        "Each country should have the key `name` and `population`"
    ):
        print(chunk, end="|", flush=True)

asyncio.run(astream_func())
# 2. --------------------------------------------------
# France|Spain|Japan|