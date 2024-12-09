from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

chat_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=150,
)    

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of Korea?"}
]

result = chat_model.invoke(messages)
print(result.content)
# Korea is divided into two countries: South Korea and North Korea. The capital of South Korea is Seoul, while the capital of North Korea is Pyongyang.