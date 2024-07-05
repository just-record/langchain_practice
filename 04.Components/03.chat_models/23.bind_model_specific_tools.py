from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

model = ChatOpenAI()

model_with_tools = model.bind(
    tools=[
        {
            "type": "function",
            "function": {
                "name": "multiply",
                "description": "Multiply two integers together.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First integer"},
                        "b": {"type": "number", "description": "Second integer"},
                    },
                    "required": ["a", "b"],
                },
            },
        }
    ]
)

results = model_with_tools.invoke("Whats 119 times 8?")
print(results.tool_calls)
# [{'name': 'multiply', 'args': {'a': 119, 'b': 8}, 'id': 'call_GK6SldegUL9ACByw3vfoYxDQ'}]