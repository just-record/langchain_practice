from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

# from langchain_anthropic.chat_models import ChatAnthropic
from langchain_openai.chat_models import ChatOpenAI

# chat = ChatAnthropic(model="claude-3-haiku-20240307")
chat = ChatOpenAI(model="gpt-4o-mini")


#################################################################################
### 1. sync streaming
print('1.', '-' * 50)
##################################################################################
for chunk in chat.stream("Write me a 1 verse song about goldfish on the moon"):
    print(chunk.content, end="|", flush=True)
# |(|Verse|)|  
# |In| a| silver| sea| on| the| moon|light|'s| glow|,|  
# |Gold|fish| dance| where| the| st|ard|ust| flows|,|  
# |Floating| free| in| a| cosmic| dream|,|  
# |W|aving| fins| in| a| lunar| stream|,|  
# |With| bubbles| pop|pin|’| like| a| dream|er's| tune|,|  
# |Making| wishes| '|neath| the| pale| blue| moon|.||    


#################################################################################
### 2. async streaming
print('2.', '-' * 50)
##################################################################################
async def astream_func():
    async for chunk in chat.astream("Write me a 1 verse song about goldfish on the moon"):
        print(chunk.content, end="|", flush=True)

import asyncio
asyncio.run(astream_func())    
# 2. --------------------------------------------------
# |(|Verse|)|  
# |In| a| silver| bowl| under| st|arl|it| skies|,|  
# |Gold|fish| swim| in| dreams| where| the| lunar| light| lies|,|  
# |B|ubbles| dance| like| whispers|,| in| the| weight|less| tune|,|  
# |Floating| free| in| wonder|,| those| gold|fish| on| the| moon|.|  ||    


#################################################################################
### 3. astream events
print('3.', '-' * 50)
##################################################################################
idx = 0

async def astream_events_func():
    async for event in chat.astream_events(
        "Write me a 1 verse song about goldfish on the moon", version="v1"
    ):
        global idx
        idx += 1
        if idx >= 5:  # Truncate the output
            print("...Truncated")
            break
        print(event)

import asyncio
asyncio.run(astream_events_func())        
# 3. --------------------------------------------------
# {'event': 'on_chat_model_start', 'run_id': '229d2b24-5d82-4f6d-a9a9-e78e97a5c312', 'name': 'ChatOpenAI', 'tags': [], 'metadata': {}, 'data': {'input': 'Write me a 1 verse song about goldfish on the moon'}, 'parent_ids': []}
# {'event': 'on_chat_model_stream', 'run_id': '229d2b24-5d82-4f6d-a9a9-e78e97a5c312', 'tags': [], 'metadata': {}, 'name': 'ChatOpenAI', 'data': {'chunk': AIMessageChunk(content='', additional_kwargs={}, response_metadata={}, id='run-229d2b24-5d82-4f6d-a9a9-e78e97a5c312')}, 'parent_ids': []}
# {'event': 'on_chat_model_stream', 'run_id': '229d2b24-5d82-4f6d-a9a9-e78e97a5c312', 'tags': [], 'metadata': {}, 'name': 'ChatOpenAI', 'data': {'chunk': AIMessageChunk(content='(', additional_kwargs={}, response_metadata={}, id='run-229d2b24-5d82-4f6d-a9a9-e78e97a5c312')}, 'parent_ids': []}
# {'event': 'on_chat_model_stream', 'run_id': '229d2b24-5d82-4f6d-a9a9-e78e97a5c312', 'tags': [], 'metadata': {}, 'name': 'ChatOpenAI', 'data': {'chunk': AIMessageChunk(content='Verse', additional_kwargs={}, response_metadata={}, id='run-229d2b24-5d82-4f6d-a9a9-e78e97a5c312')}, 'parent_ids': []}
# ...Truncated