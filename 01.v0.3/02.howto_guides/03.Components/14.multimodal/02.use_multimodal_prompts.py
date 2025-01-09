# 여기서는 모델에 멀티모달 입력을 포맷하기 위한 프롬프트 템플릿 사용 방법을 보여드립니다.
# 이 예시에서는 모델에게 이미지를 설명하도록 요청할 것입니다.

from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

import base64

import httpx

### 이미지를 base64로 인코딩 ###
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")


### model 및 chat prompt 생성 ###
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Describe the image provided"),
        (
            "user",
            [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
                }
            ],
        ),
    ]
)

### chaining ###
chain = prompt | model


#################################################################################
### 1. chain invoke
print('1.', '-' * 50)
#################################################################################
response = chain.invoke({"image_data": image_data})
rprint(response)
# 1. --------------------------------------------------
# AIMessage(
#     content='The image depicts a scenic landscape with a wooden boardwalk leading through a lush field of tall green grass. The sky is a vibrant blue, adorned with scattered, wispy clouds. In 
# the background, there are dense clusters of trees and bushes, suggesting a peaceful, natural setting. The lighting gives a warm and inviting atmosphere, indicating a sunny day.',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 71,
#             'prompt_tokens': 1164,
#             'total_tokens': 1235,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-2024-08-06',
#         'system_fingerprint': 'fp_b7d65f1a5b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-bd3c775d-5cdb-40dd-b5fd-73d796605595-0',
#     usage_metadata={
#         'input_tokens': 1164,
#         'output_tokens': 71,
#         'total_tokens': 1235,
#         'input_token_details': {'audio': 0, 'cache_read': 0},
#         'output_token_details': {'audio': 0, 'reasoning': 0}
#     }
# )


#################################################################################
### 2. multiple images
print('2.', '-' * 50)
#################################################################################
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "compare the two pictures provided"),
        (
            "user",
            [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image_data1}"},
                },
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image_data2}"},
                },
            ],
        ),
    ]
)

chain = prompt | model

response = chain.invoke({"image_data1": image_data, "image_data2": image_data})
rprint(response)
# 2. --------------------------------------------------
# AIMessage(
#     content='The two images are identical. They both depict a wooden pathway leading through a green meadow under a blue sky with scattered clouds. The lighting and composition are the same in 
# each image.',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 37,
#             'prompt_tokens': 2073,
#             'total_tokens': 2110,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-2024-08-06',
#         'system_fingerprint': 'fp_5f20662549',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-b01f2043-5757-4fd5-b362-430e27c74dc6-0',
#     usage_metadata={
#         'input_tokens': 2073,
#         'output_tokens': 37,
#         'total_tokens': 2110,
#         'input_token_details': {'audio': 0, 'cache_read': 0},
#         'output_token_details': {'audio': 0, 'reasoning': 0}
#     }
# )