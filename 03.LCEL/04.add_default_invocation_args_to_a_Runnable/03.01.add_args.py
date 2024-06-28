from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

model = ChatOpenAI(model="gpt-3.5-turbo").bind(tools=tools)


### tools 사용이 필요 없는 질문
results = model.invoke("What is the capital of South Korea?")
print(results)

print('-' * 50)

### tools 사용이 필요한 질문 - 실제 tools에 해당하는 함수를 선언 후에
def get_current_weather(location, unit="celsius"):
    return f"The current weather in {location} is 25 degrees {unit}."


results = model.invoke("What's the weather in SF, NYC and LA?")
print(results)


