from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

##################################################################################
### 1. stream
print('1.', '-' * 50)
##################################################################################
chunks = []
for chunk in model.stream("what color is the sky?"):
    chunks.append(chunk)
    print(chunk.content, end="|", flush=True)
# 1. --------------------------------------------------
# |The| color| of| the| sky| can| vary| depending| on| several| factors|,| including| the| time| of| day|,| weather| conditions|,| and| atmospheric| particles|.| Typically|,| during| the| day|,| the| sky| appears| blue| due| to| Ray|leigh| scattering|,| where| shorter| blue| wavelengths| of| sunlight| are| scattered| in| all| directions| by| the| gases| and| particles| in| the| Earth's| atmosphere|.| At| sunrise| and| sunset|,| the| sky| can| take| on| shades| of| red|,| orange|,| and| pink| due| to| the| longer| path| of| sunlight| through| the| atmosphere|,| which| scat|ters| the| shorter| wavelengths| and| allows| the| longer| wavelengths| to| dominate|.| On| cloudy| or| over|cast| days|,| the| sky| may| appear| gray|.||


##################################################################################
### 2. 비동기 환경 일 때 - async
print('2.', '-' * 50)
##################################################################################
import asyncio

chunks = []
async def astream_func():
    async for chunk in model.astream("what color is the sky?"):
        chunks.append(chunk)
        print(chunk.content, end="|", flush=True)
        
asyncio.run(astream_func())
# 2. --------------------------------------------------
# |The| color| of| the| sky| can| vary| depending| on| several| factors|,| including| the| time| of| day|,| weather| conditions|,| and| atmospheric| particles|.| Generally|,| during| a| clear| day|,| the| sky| appears| blue| due| to| the| scattering| of| sunlight| by| the| Earth's| atmosphere|.| At| sunrise| and| sunset|,| the| sky| can| display| a| range| of| colors|,| including| shades| of| orange|,| pink|,| and| purple|,| as| the| light| passes| through| a| thicker| layer| of| atmosphere|.| On| cloudy| or| over|cast| days|,| the| sky| may| appear| gray|.| Other| factors|,| such| as| pollution| or| dust|,| can| also| affect| its| color|.||(langchain_practice) dev01@ubn-service-01:~/app/source_code/langchain_practice/01.v0.3/02.howto_guides/01.key_features/03.stream_runnables$ 


##################################################################################
### 3. chunks[0] 확인
print('3.', '-' * 50)
##################################################################################
rprint(chunks[0])
# 3. --------------------------------------------------
# AIMessageChunk(content='', additional_kwargs={}, response_metadata={}, id='run-b6120422-523a-4a42-b0e8-bb84547e1d1c')


##################################################################################
### 4. chunks 더하기
print('4.', '-' * 50)
##################################################################################
rprint(chunks[0] + chunks[1] + chunks[2] + chunks[3] + chunks[4])
# 4. --------------------------------------------------
# AIMessageChunk(content='The color of the', additional_kwargs={}, response_metadata={}, id='run-449dcf79-aba1-41dc-a7cd-d799f87702f0')
