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
### 또는 아래와 같이 bind_tools를 사용할 수 있습니다.
# model = ChatOpenAI(model="gpt-3.5-turbo").bind_tools(tools)


results = model.invoke("What's the weather in SF, NYC and LA?")
print(results)
