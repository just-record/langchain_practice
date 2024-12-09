from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

result = llm.invoke("hi")
rprint(result)
# AIMessage(
#     content='Hello! How can I assist you today?',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 9,
#             'prompt_tokens': 8,
#             'total_tokens': 17,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-3.5-turbo-0125',
#         'system_fingerprint': None,
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-6e406fda-860f-46fa-834e-f51214173f00-0',
#     usage_metadata={'input_tokens': 8, 'output_tokens': 9, 'total_tokens': 17, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )