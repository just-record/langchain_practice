from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

#################################################################################
### 1. tool schema의 포맷 - 제공업체마다 다름
### openai의 예시
print('1.', '-' * 50)
##################################################################################
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

rprint(model_with_tools.invoke("Whats 119 times 8?"))
# 1. --------------------------------------------------
# AIMessage(
#     content='',
#     additional_kwargs={
#         'tool_calls': [
#             {'id': 'call_Te9WlJKaEzbR1GCdBNVNL7j2', 'function': {'arguments': '{"a": 119, "b": 8}', 'name': 'multiply'}, 'type': 'function'},
#             {'id': 'call_zFvs5QiAjToRK5vaEdfu8Wax', 'function': {'arguments': '{"a": 8, "b": 119}', 'name': 'multiply'}, 'type': 'function'}
#         ],
#         'refusal': None
#     },
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 50,
#             'prompt_tokens': 62,
#             'total_tokens': 112,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-3.5-turbo-0125',
#         'system_fingerprint': None,
#         'finish_reason': 'tool_calls',
#         'logprobs': None
#     },
#     id='run-7cc8079e-1390-4486-8293-8e2fea41f8b0-0',
#     tool_calls=[
#         {'name': 'multiply', 'args': {'a': 119, 'b': 8}, 'id': 'call_Te9WlJKaEzbR1GCdBNVNL7j2', 'type': 'tool_call'},
#         {'name': 'multiply', 'args': {'a': 8, 'b': 119}, 'id': 'call_zFvs5QiAjToRK5vaEdfu8Wax', 'type': 'tool_call'}
#     ],
#     usage_metadata={'input_tokens': 62, 'output_tokens': 50, 'total_tokens': 112, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )