from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

chat = ChatOpenAI(model="gpt-3.5-turbo")

### 1. stream
for chunk in chat.stream("Write me a 1 verse song about goldfish on the moon"):
    print(chunk.content, end="|", flush=True)
print('')
# |Sw|imming| through| space|,| in| a| cosmic| ballet|
# |Gold|fish| on| the| moon|,| shining| bright| as| day||    


### 2.astream
print('-'*30)

async def chat_astream():
    async for chunk in chat.astream("Write me a 1 verse song about goldfish on the moon"):
        print(chunk.content, end="|", flush=True)

import asyncio
asyncio.run(chat_astream())
print('')


### 3. astream events
# pass
