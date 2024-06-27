from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")

events = []
async def stream_events():
    async for event in model.astream_events("hello", version="v2"):
        events.append(event)

import asyncio
asyncio.run(stream_events())

print(events[:3])
print('-' * 50)
print(events[-2:])