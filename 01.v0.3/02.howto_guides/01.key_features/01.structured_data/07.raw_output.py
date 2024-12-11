from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from typing import Optional
from typing_extensions import Annotated, TypedDict

from langchain_openai import ChatOpenAI


# llm = ChatOpenAI(model="gpt-4o-mini")
llm = ChatOpenAI(model="gpt-4o")

##################################################################################
### 1. include_raw=True
print('1.', '-' * 50)
##################################################################################
class Joke(TypedDict):
    """Joke to tell user."""

    setup: Annotated[str, ..., "The setup of the joke"]

    # Alternatively, we could have specified setup as:

    # setup: str                    # no default, no description
    # setup: Annotated[str, ...]    # no default, no description
    # setup: Annotated[str, "foo"]  # default, no description

    punchline: Annotated[str, ..., "The punchline of the joke"]
    ### `...`는 pass 느낌. 빈칸으로 두지 않고 Ellipsis(`...`)를 사용하여 가독성을 높이고 의도를 명확히 할 수 있다. ###
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]


structured_llm = llm.with_structured_output(Joke, include_raw=True)
results = structured_llm.invoke("Tell me a joke about cats")
rprint(results)
# 1. --------------------------------------------------
# {
#     'raw': AIMessage(
#         content='',
#         additional_kwargs={
#             'tool_calls': [
#                 {
#                     'id': 'call_v7DlFZZL8b8DpqIHBWO6kiIc',
#                     'function': {
#                         'arguments': '{"setup":"Why did the cat sit on the computer?","punchline":"Because it wanted to keep an eye on the mouse!","rating":7}',
#                         'name': 'Joke'
#                     },
#                     'type': 'function'
#                 }
#             ],
#             'refusal': None
#         },
#         response_metadata={
#             'token_usage': {
#                 'completion_tokens': 33,
#                 'prompt_tokens': 93,
#                 'total_tokens': 126,
#                 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#                 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#             },
#             'model_name': 'gpt-4o-2024-08-06',
#             'system_fingerprint': 'fp_9d50cd990b',
#             'finish_reason': 'stop',
#             'logprobs': None
#         },
#         id='run-d14de6c0-ffff-4fd7-b993-63e2cca5c9a3-0',
#         tool_calls=[
#             {
#                 'name': 'Joke',
#                 'args': {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep an eye on the mouse!', 'rating': 7},
#                 'id': 'call_v7DlFZZL8b8DpqIHBWO6kiIc',
#                 'type': 'tool_call'
#             }
#         ],
#         usage_metadata={
#             'input_tokens': 93,
#             'output_tokens': 33,
#             'total_tokens': 126,
#             'input_token_details': {'audio': 0, 'cache_read': 0},
#             'output_token_details': {'audio': 0, 'reasoning': 0}
#         }
#     ),
#     'parsed': {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep an eye on the mouse!', 'rating': 7},
#     'parsing_error': None
# }
