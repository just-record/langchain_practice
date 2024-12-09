from dotenv import load_dotenv
load_dotenv()

# OpenAI의 Chat 모델
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")

chunks = []
for chunk in model.stream("what color is the sky?"):
    chunks.append(chunk)
    print(chunk.content, end="|", flush=True)

print('-' * 50)

print(chunks[0])

print('-' * 50)

print(chunks[0] + chunks[1] + chunks[2] + chunks[3] + chunks[4])
