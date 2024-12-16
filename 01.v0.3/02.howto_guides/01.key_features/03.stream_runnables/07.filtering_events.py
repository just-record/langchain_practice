from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
import asyncio

model = ChatOpenAI(model="gpt-4o-mini")

#################################################################################
### 1. 이벤트 필터링 - 필터 없음
print('1.', '-' * 50)
##################################################################################
chain = model.with_config({"run_name": "model"}) | JsonOutputParser().with_config(
    {"run_name": "my_parser"}
)

max_events = 0

async def astream_events_func():
    async for event in chain.astream_events(
        "output a list of the countries france, spain and japan and their populations in JSON format. "
        'Use a dict with an outer key of "countries" which contains a list of countries. '
        "Each country should have the key `name` and `population`",
        version="v2",
        include_names=["my_parser"],
    ):
        global max_events
        print(event)
        max_events += 1
        if max_events > 10:
            # Truncate output
            print("...")
            break
        
asyncio.run(astream_events_func())
# 1. --------------------------------------------------
# {'event': 'on_parser_start', 'data': {'input': 'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`'}, 'name': 'my_parser', 'tags': ['seq:step:2'], 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'metadata': {}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# {'event': 'on_parser_stream', 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'name': 'my_parser', 'tags': ['seq:step:2'], 'metadata': {}, 'data': {'chunk': {}}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# {'event': 'on_parser_stream', 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'name': 'my_parser', 'tags': ['seq:step:2'], 'metadata': {}, 'data': {'chunk': {'countries': []}}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# {'event': 'on_parser_stream', 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'name': 'my_parser', 'tags': ['seq:step:2'], 'metadata': {}, 'data': {'chunk': {'countries': [{}]}}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# {'event': 'on_parser_stream', 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'name': 'my_parser', 'tags': ['seq:step:2'], 'metadata': {}, 'data': {'chunk': {'countries': [{'name': ''}]}}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# {'event': 'on_parser_stream', 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'name': 'my_parser', 'tags': ['seq:step:2'], 'metadata': {}, 'data': {'chunk': {'countries': [{'name': 'France'}]}}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# {'event': 'on_parser_stream', 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'name': 'my_parser', 'tags': ['seq:step:2'], 'metadata': {}, 'data': {'chunk': {'countries': [{'name': 'France', 'population': 652}]}}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# {'event': 'on_parser_stream', 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'name': 'my_parser', 'tags': ['seq:step:2'], 'metadata': {}, 'data': {'chunk': {'countries': [{'name': 'France', 'population': 652735}]}}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# {'event': 'on_parser_stream', 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'name': 'my_parser', 'tags': ['seq:step:2'], 'metadata': {}, 'data': {'chunk': {'countries': [{'name': 'France', 'population': 65273511}]}}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# {'event': 'on_parser_stream', 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'name': 'my_parser', 'tags': ['seq:step:2'], 'metadata': {}, 'data': {'chunk': {'countries': [{'name': 'France', 'population': 65273511}, {}]}}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# {'event': 'on_parser_stream', 'run_id': '11432d73-c6a3-405f-92a4-581ce8d0c333', 'name': 'my_parser', 'tags': ['seq:step:2'], 'metadata': {}, 'data': {'chunk': {'countries': [{'name': 'France', 'population': 65273511}, {'name': ''}]}}, 'parent_ids': ['79c76635-8ff8-491f-b164-42ee1ce8a536']}
# ...


#################################################################################
### 2. 이벤트 필터링
### 타입에 의한 필터링
print('2.', '-' * 50)
##################################################################################
chain = model.with_config({"run_name": "model"}) | JsonOutputParser().with_config(
    {"run_name": "my_parser"}
)

max_events = 0
async def astream_events_func():
    async for event in chain.astream_events(
        'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`',
        version="v2",
        include_types=["chat_model"],
    ):
        global max_events
        print(event)
        max_events += 1
        if max_events > 10:
            # Truncate output
            print("...")
            break
        
asyncio.run(astream_events_func())        
# 2. --------------------------------------------------
# {'event': 'on_chat_model_start', 'data': {'input': 'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`'}, 'name': 'model', 'tags': ['seq:step:1'], 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content='', additional_kwargs={}, response_metadata={}, id='run-368bd55c-04db-481f-a4d3-bf7f578377de')}, 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'name': 'model', 'tags': ['seq:step:1'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content='Here', additional_kwargs={}, response_metadata={}, id='run-368bd55c-04db-481f-a4d3-bf7f578377de')}, 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'name': 'model', 'tags': ['seq:step:1'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' is', additional_kwargs={}, response_metadata={}, id='run-368bd55c-04db-481f-a4d3-bf7f578377de')}, 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'name': 'model', 'tags': ['seq:step:1'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' the', additional_kwargs={}, response_metadata={}, id='run-368bd55c-04db-481f-a4d3-bf7f578377de')}, 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'name': 'model', 'tags': ['seq:step:1'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' JSON', additional_kwargs={}, response_metadata={}, id='run-368bd55c-04db-481f-a4d3-bf7f578377de')}, 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'name': 'model', 'tags': ['seq:step:1'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' representation', additional_kwargs={}, response_metadata={}, id='run-368bd55c-04db-481f-a4d3-bf7f578377de')}, 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'name': 'model', 'tags': ['seq:step:1'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' of', additional_kwargs={}, response_metadata={}, id='run-368bd55c-04db-481f-a4d3-bf7f578377de')}, 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'name': 'model', 'tags': ['seq:step:1'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' the', additional_kwargs={}, response_metadata={}, id='run-368bd55c-04db-481f-a4d3-bf7f578377de')}, 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'name': 'model', 'tags': ['seq:step:1'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' countries', additional_kwargs={}, response_metadata={}, id='run-368bd55c-04db-481f-a4d3-bf7f578377de')}, 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'name': 'model', 'tags': ['seq:step:1'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' France', additional_kwargs={}, response_metadata={}, id='run-368bd55c-04db-481f-a4d3-bf7f578377de')}, 'run_id': '368bd55c-04db-481f-a4d3-bf7f578377de', 'name': 'model', 'tags': ['seq:step:1'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['b988d63b-1590-44be-8819-138b5297e377']}
# ...


#################################################################################
### 3. 이벤트 필터링
### 태그에 의한 필터링
print('3.', '-' * 50)
##################################################################################
chain = (model | JsonOutputParser()).with_config({"tags": ["my_chain"]})

max_events = 0
async def astream_events_func():
    async for event in chain.astream_events(
        'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`',
        version="v2",
        include_tags=["my_chain"],
    ):
        global max_events
        print(event)
        max_events += 1
        if max_events > 10:
            # Truncate output
            print("...")
            break
        
asyncio.run(astream_events_func())        
# 3. --------------------------------------------------
# {'event': 'on_chain_start', 'data': {'input': 'output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`'}, 'name': 'RunnableSequence', 'tags': ['my_chain'], 'run_id': '6ec28be2-ae00-467a-9bd1-ffeeda71e661', 'metadata': {}, 'parent_ids': []}
# {'event': 'on_chat_model_start', 'data': {'input': {'messages': [[HumanMessage(content='output a list of the countries france, spain and japan and their populations in JSON format. Use a dict with an outer key of "countries" which contains a list of countries. Each country should have the key `name` and `population`', additional_kwargs={}, response_metadata={})]]}}, 'name': 'ChatOpenAI', 'tags': ['seq:step:1', 'my_chain'], 'run_id': '8631a6a5-d26d-474f-b8f7-c7152b6f3257', 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['6ec28be2-ae00-467a-9bd1-ffeeda71e661']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content='', additional_kwargs={}, response_metadata={}, id='run-8631a6a5-d26d-474f-b8f7-c7152b6f3257')}, 'run_id': '8631a6a5-d26d-474f-b8f7-c7152b6f3257', 'name': 'ChatOpenAI', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['6ec28be2-ae00-467a-9bd1-ffeeda71e661']}
# {'event': 'on_parser_start', 'data': {}, 'name': 'JsonOutputParser', 'tags': ['seq:step:2', 'my_chain'], 'run_id': 'f9007482-fefa-4483-b98c-e55fbe950dd4', 'metadata': {}, 'parent_ids': ['6ec28be2-ae00-467a-9bd1-ffeeda71e661']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content='Here', additional_kwargs={}, response_metadata={}, id='run-8631a6a5-d26d-474f-b8f7-c7152b6f3257')}, 'run_id': '8631a6a5-d26d-474f-b8f7-c7152b6f3257', 'name': 'ChatOpenAI', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['6ec28be2-ae00-467a-9bd1-ffeeda71e661']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' is', additional_kwargs={}, response_metadata={}, id='run-8631a6a5-d26d-474f-b8f7-c7152b6f3257')}, 'run_id': '8631a6a5-d26d-474f-b8f7-c7152b6f3257', 'name': 'ChatOpenAI', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['6ec28be2-ae00-467a-9bd1-ffeeda71e661']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' the', additional_kwargs={}, response_metadata={}, id='run-8631a6a5-d26d-474f-b8f7-c7152b6f3257')}, 'run_id': '8631a6a5-d26d-474f-b8f7-c7152b6f3257', 'name': 'ChatOpenAI', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['6ec28be2-ae00-467a-9bd1-ffeeda71e661']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' requested', additional_kwargs={}, response_metadata={}, id='run-8631a6a5-d26d-474f-b8f7-c7152b6f3257')}, 'run_id': '8631a6a5-d26d-474f-b8f7-c7152b6f3257', 'name': 'ChatOpenAI', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['6ec28be2-ae00-467a-9bd1-ffeeda71e661']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' JSON', additional_kwargs={}, response_metadata={}, id='run-8631a6a5-d26d-474f-b8f7-c7152b6f3257')}, 'run_id': '8631a6a5-d26d-474f-b8f7-c7152b6f3257', 'name': 'ChatOpenAI', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['6ec28be2-ae00-467a-9bd1-ffeeda71e661']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' format', additional_kwargs={}, response_metadata={}, id='run-8631a6a5-d26d-474f-b8f7-c7152b6f3257')}, 'run_id': '8631a6a5-d26d-474f-b8f7-c7152b6f3257', 'name': 'ChatOpenAI', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['6ec28be2-ae00-467a-9bd1-ffeeda71e661']}
# {'event': 'on_chat_model_stream', 'data': {'chunk': AIMessageChunk(content=' containing', additional_kwargs={}, response_metadata={}, id='run-8631a6a5-d26d-474f-b8f7-c7152b6f3257')}, 'run_id': '8631a6a5-d26d-474f-b8f7-c7152b6f3257', 'name': 'ChatOpenAI', 'tags': ['seq:step:1', 'my_chain'], 'metadata': {'ls_provider': 'openai', 'ls_model_name': 'gpt-4o-mini', 'ls_model_type': 'chat', 'ls_temperature': 0.7}, 'parent_ids': ['6ec28be2-ae00-467a-9bd1-ffeeda71e661']}
# ...