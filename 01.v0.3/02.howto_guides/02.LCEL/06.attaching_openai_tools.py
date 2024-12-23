from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

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

model = ChatOpenAI(model="gpt-4o-mini").bind(tools=tools)
results = model.invoke("What's the weather in SF, NYC and LA?")
rprint(results)
# AIMessage(
#     content='',
#     additional_kwargs={
#         'tool_calls': [
#             {'id': 'call_roRTxcNJGOigDn9Kqmxrp6sR', 'function': {'arguments': '{"location": "San Francisco, CA"}', 'name': 'get_current_weather'}, 'type': 'function'},
#             {'id': 'call_BNlm6X71a0YLSvynoSCHeFvl', 'function': {'arguments': '{"location": "New York City, NY"}', 'name': 'get_current_weather'}, 'type': 'function'},
#             {'id': 'call_urb3pT3UCnxlT3r2XJ29Lym2', 'function': {'arguments': '{"location": "Los Angeles, CA"}', 'name': 'get_current_weather'}, 'type': 'function'}
#         ],
#         'refusal': None
#     },
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 72,
#             'prompt_tokens': 82,
#             'total_tokens': 154,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_0aa8d3e20b',
#         'finish_reason': 'tool_calls',
#         'logprobs': None
#     },
#     id='run-f5a5c4c9-20e7-4182-8802-a20de2c3d25b-0',
#     tool_calls=[
#         {'name': 'get_current_weather', 'args': {'location': 'San Francisco, CA'}, 'id': 'call_roRTxcNJGOigDn9Kqmxrp6sR', 'type': 'tool_call'},
#         {'name': 'get_current_weather', 'args': {'location': 'New York City, NY'}, 'id': 'call_BNlm6X71a0YLSvynoSCHeFvl', 'type': 'tool_call'},
#         {'name': 'get_current_weather', 'args': {'location': 'Los Angeles, CA'}, 'id': 'call_urb3pT3UCnxlT3r2XJ29Lym2', 'type': 'tool_call'}
#     ],
#     usage_metadata={'input_tokens': 82, 'output_tokens': 72, 'total_tokens': 154, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )