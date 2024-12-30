from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI


#################################################################################
### 1. Response metadata - openai
print('1.', '-' * 50)
##################################################################################
# llm = ChatOpenAI(model="gpt-4o-mini")
# msg = llm.invoke([("human", "What's the oldest known example of cuneiform")])
# rprint(msg.response_metadata)
# 1. --------------------------------------------------
# {
#     'token_usage': {
#         'completion_tokens': 100,
#         'prompt_tokens': 16,
#         'total_tokens': 116,
#         'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#         'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#     },
#     'model_name': 'gpt-4o-mini-2024-07-18',
#     'system_fingerprint': 'fp_d02d531b47',
#     'finish_reason': 'stop',
#     'logprobs': None
# }


#################################################################################
### 2. Response metadata - anthropic
print('2.', '-' * 50)
##################################################################################
# from langchain_anthropic import ChatAnthropic

# llm = ChatAnthropic(model="claude-3-sonnet-20240229")
# msg = llm.invoke([("human", "What's the oldest known example of cuneiform")])
# rprint(msg.response_metadata)
# 2. --------------------------------------------------
# {
#     'id': 'msg_01Ufj1xaVbqWJU5thc6YSjGs',
#     'model': 'claude-3-sonnet-20240229',
#     'stop_reason': 'end_turn',
#     'stop_sequence': None,
#     'usage': {'input_tokens': 17, 'output_tokens': 301, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}
# }


#################################################################################
### 3. Response metadata - 
### 실습 생략 - API KEY가 필요 함
print('3.', '-' * 50)
##################################################################################
# from langchain_google_vertexai import ChatVertexAI

# llm = ChatVertexAI(model="gemini-pro")
# msg = llm.invoke([("human", "What's the oldest known example of cuneiform")])
# rprint(msg.response_metadata)

# {'is_blocked': False,
#  'safety_ratings': [{'category': 'HARM_CATEGORY_HATE_SPEECH',
#    'probability_label': 'NEGLIGIBLE',
#    'blocked': False},
#   {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
#    'probability_label': 'NEGLIGIBLE',
#    'blocked': False},
#   {'category': 'HARM_CATEGORY_HARASSMENT',
#    'probability_label': 'NEGLIGIBLE',
#    'blocked': False},
#   {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
#    'probability_label': 'NEGLIGIBLE',
#    'blocked': False}],
#  'citation_metadata': None,
#  'usage_metadata': {'prompt_token_count': 10,
#   'candidates_token_count': 30,
#   'total_token_count': 40}}

#################################################################
# from langchain_aws import ChatBedrock

# llm = ChatBedrock(model_id="anthropic.claude-v2")
# msg = llm.invoke([("human", "What's the oldest known example of cuneiform")])
# rprint(msg.response_metadata)

# {'model_id': 'anthropic.claude-v2',
#  'usage': {'prompt_tokens': 19, 'completion_tokens': 371, 'total_tokens': 390}}


#################################################################
# from langchain_mistralai import ChatMistralAI

# llm = ChatMistralAI()
# msg = llm.invoke([("human", "What's the oldest known example of cuneiform")])
# rprint(msg.response_metadata)

# {'token_usage': {'prompt_tokens': 19,
#   'total_tokens': 141,
#   'completion_tokens': 122},
#  'model': 'mistral-small',
#  'finish_reason': 'stop'}


#################################################################
# from langchain_groq import ChatGroq

# llm = ChatGroq()
# msg = llm.invoke([("human", "What's the oldest known example of cuneiform")])
# rprint(msg.response_metadata)

# {'token_usage': {'completion_time': 0.243,
#   'completion_tokens': 132,
#   'prompt_time': 0.022,
#   'prompt_tokens': 22,
#   'queue_time': None,
#   'total_time': 0.265,
#   'total_tokens': 154},
#  'model_name': 'mixtral-8x7b-32768',
#  'system_fingerprint': 'fp_7b44c65f25',
#  'finish_reason': 'stop',
#  'logprobs': None}


#################################################################
# import os
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(
#     base_url="https://api.together.xyz/v1",
#     api_key=os.environ["TOGETHER_API_KEY"],
#     model="mistralai/Mixtral-8x7B-Instruct-v0.1",
# )
# msg = llm.invoke([("human", "What's the oldest known example of cuneiform")])
# rprint(msg.response_metadata)

# {'token_usage': {'completion_tokens': 208,
#   'prompt_tokens': 20,
#   'total_tokens': 228},
#  'model_name': 'mistralai/Mixtral-8x7B-Instruct-v0.1',
#  'system_fingerprint': None,
#  'finish_reason': 'eos',
#  'logprobs': None}


#################################################################
# from langchain_fireworks import ChatFireworks

# llm = ChatFireworks(model="accounts/fireworks/models/mixtral-8x7b-instruct")
# msg = llm.invoke([("human", "What's the oldest known example of cuneiform")])
# rprint(msg.response_metadata)

# {'token_usage': {'prompt_tokens': 19,
#   'total_tokens': 219,
#   'completion_tokens': 200},
#  'model_name': 'accounts/fireworks/models/mixtral-8x7b-instruct',
#  'system_fingerprint': '',
#  'finish_reason': 'length',
#  'logprobs': None}