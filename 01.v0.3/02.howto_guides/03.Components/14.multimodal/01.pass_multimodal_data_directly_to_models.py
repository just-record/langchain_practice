# 멀티모달 입력을 모델에 직접 전달하는 방법
# 현재 모든 입력은 OpenAI가 기대하는 형식과 동일한 형식으로 전달
# 멀티모달 입력을 지원하는 다른 모델 제공업체의 경우, 클래스 내부에 예상되는 형식으로 변환하는 로직을 추가

from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

### image url ###
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

### model ###
model = ChatOpenAI(model="gpt-4o")

#################################################################################
### 1. multimodat data를 모델에 직접 전달
### 이미지를 전달하는 가장 일반적으로 지원되는 방법은 바이트 문자열(byte string)로 전달하는 것. 대부분의 모델 통합에서 작동.
#################################################################################
import base64

import httpx

image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")


#################################################################################
### 1-1. message 생성하고 모델 invoke
print('1-1.', '-' * 50)
#################################################################################
message = HumanMessage(
    content=[
        {"type": "text", "text": "describe the weather in this image"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
        },
    ],
)
response = model.invoke([message])
rprint(response)
# 1-1. --------------------------------------------------
# AIMessage(
#     content="The weather in the image appears to be clear and sunny. The sky is mostly blue with a few scattered clouds, indicating a pleasant day. The lighting suggests it's likely daytime, 
# with the sun casting bright light on the green grass and surrounding landscape.",
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 50,
#             'prompt_tokens': 1151,
#             'total_tokens': 1201,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-2024-08-06',
#         'system_fingerprint': 'fp_b7d65f1a5b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-ebc5ec73-4b9c-4034-8a49-ed910798e49d-0',
#     usage_metadata={
#         'input_tokens': 1151,
#         'output_tokens': 50,
#         'total_tokens': 1201,
#         'input_token_details': {'audio': 0, 'cache_read': 0},
#         'output_token_details': {'audio': 0, 'reasoning': 0}
#     }
# )


#################################################################################
### 1-2. 이미지 URL을 직접 입력 - 일부 모델 제공업체만 이 기능을 지원
print('1-2.', '-' * 50)
#################################################################################
message = HumanMessage(
    content=[
        {"type": "text", "text": "describe the weather in this image"},
        {"type": "image_url", "image_url": {"url": image_url}},
    ],
)
response = model.invoke([message])
rprint(response.content)
# 1-2. --------------------------------------------------
# The weather in the image appears to be clear and sunny. The sky is mostly blue with some scattered clouds, suggesting a pleasant day with good visibility. The landscape is well-lit, indicating 
# daylight and likely mild temperatures.


#################################################################################
### 1-3. multiple images
print('1-3.', '-' * 50)
#################################################################################
message = HumanMessage(
    content=[
        {"type": "text", "text": "are these two images the same?"},
        {"type": "image_url", "image_url": {"url": image_url}},
        {"type": "image_url", "image_url": {"url": image_url}},
    ],
)
response = model.invoke([message])
rprint(response.content)
# 1-3. --------------------------------------------------
# Yes, the two images are the same.


#################################################################################
### 2. Tool calls
### 일부 멀티모달 모델들은 도구 호출 기능도 지원
### 도구들을 모델에 바인딩하고, 원하는 유형의 콘텐츠 블록(예: 이미지 데이터가 포함된)을 사용하여 모델을 호출
#################################################################################
from typing import Literal

from langchain_core.tools import tool


@tool
def weather_tool(weather: Literal["sunny", "cloudy", "rainy"]) -> None:
    """Describe the weather"""
    pass


model_with_tools = model.bind_tools([weather_tool])

message = HumanMessage(
    content=[
        # {"type": "text", "text": "describe the weather in this image"},
        {"type": "text", "text": "describe the weather in this image with a tool"}, # tool을 사용 하지 않아 조금 수정
        {"type": "image_url", "image_url": {"url": image_url}},
    ],
)

#################################################################################
### 2-1. tool이 바인딩 된 model invoke
print('2-1.', '-' * 50)
#################################################################################
response = model_with_tools.invoke([message])
rprint(response)
# 2-1. --------------------------------------------------
# AIMessage(
#     content='',
#     additional_kwargs={'tool_calls': [{'id': 'call_YJnyjXRKUHSPLYjEJ0torpMO', 'function': {'arguments': '{"weather":"sunny"}', 'name': 'weather_tool'}, 'type': 'function'}], 'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 16,
#             'prompt_tokens': 1197,
#             'total_tokens': 1213,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-2024-08-06',
#         'system_fingerprint': 'fp_b7d65f1a5b',
#         'finish_reason': 'tool_calls',
#         'logprobs': None
#     },
#     id='run-c62cbd19-a815-4c8b-b1f5-10a8b2c15464-0',
#     tool_calls=[{'name': 'weather_tool', 'args': {'weather': 'sunny'}, 'id': 'call_YJnyjXRKUHSPLYjEJ0torpMO', 'type': 'tool_call'}],
#     usage_metadata={
#         'input_tokens': 1197,
#         'output_tokens': 16,
#         'total_tokens': 1213,
#         'input_token_details': {'audio': 0, 'cache_read': 0},
#         'output_token_details': {'audio': 0, 'reasoning': 0}
#     }
# )