from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
import asyncio

model = ChatOpenAI(model="gpt-4o-mini")

#################################################################################
### 1. 스트림이 되지 않음
### '_extract_country_names'가 입력 스트림을 처리하지 않고 최종 결과 값을 return
print('1.', '-' * 50)
##################################################################################

# Function that does not support streaming.
# It operates on the finalizes inputs rather than
# operating on the input stream.
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


chain = (
    model | JsonOutputParser() | _extract_country_names
)  # This parser only works with OpenAI right now


async def astream_func():
    async for chunk in chain.astream(
        "output a list of the countries france, spain and japan and their populations in JSON format. "
        'Use a dict with an outer key of "countries" which contains a list of countries. '
        "Each country should have the key `name` and `population`",
    ):
        print(chunk, flush=True)
        
asyncio.run(astream_func())
# 1. --------------------------------------------------
# ['France', 'Spain', 'Japan']


#################################################################################
### 2. astream_events 적용
### 동일한 chain 이지만 astream_events에서는 모델과 파서에서 스트리밍 출력은 여전히 나옴
print('2.', '-' * 50)
##################################################################################
num_events = 0

async def astream_events_func():
    async for event in chain.astream_events(
        "output a list of the countries france, spain and japan and their populations in JSON format. "
        'Use a dict with an outer key of "countries" which contains a list of countries. '
        "Each country should have the key `name` and `population`",
        version="v2",
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            print(
                f"Chat model chunk: {repr(event['data']['chunk'].content)}",
                flush=True,
            )
        if kind == "on_parser_stream":
            print(f"Parser chunk: {event['data']['chunk']}", flush=True)
        global num_events
        num_events += 1
        if num_events > 30:
            # Truncate the output
            print("...")
            break
        
asyncio.run(astream_events_func())        
# 2. --------------------------------------------------
# Chat model chunk: ''
# Chat model chunk: 'Here'
# Chat model chunk: ' is'
# Chat model chunk: ' the'
# Chat model chunk: ' JSON'
# Chat model chunk: ' representation'
# Chat model chunk: ' of'
# Chat model chunk: ' the'
# Chat model chunk: ' countries'
# Chat model chunk: ' France'
# Chat model chunk: ','
# Chat model chunk: ' Spain'
# Chat model chunk: ','
# Chat model chunk: ' and'
# Chat model chunk: ' Japan'
# Chat model chunk: ' along'
# Chat model chunk: ' with'
# Chat model chunk: ' their'
# Chat model chunk: ' populations'
# Chat model chunk: ':\n\n'
# Chat model chunk: '```'
# Chat model chunk: 'json'
# Chat model chunk: '\n'
# Chat model chunk: '{\n'
# Parser chunk: {}
# Chat model chunk: ' '
# Chat model chunk: ' "'
# ...