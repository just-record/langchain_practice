from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import base64
import httpx

model = ChatOpenAI(model="gpt-4o")

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"


### 1. 이미지 data를 input으로 입력
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")

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
print(response.content)
# The weather in the image appears to be clear and pleasant. The sky is mostly blue with some scattered clouds, suggesting it is likely a sunny day with mild temperatures. The sunlight casts bright and warm light on the grassy field, giving the impression of a calm and comfortable day, possibly in late spring or summer. There is no sign of harsh weather conditions such as rain or strong winds.


### 2. 이미지 url을 input으로 입력
print('-'*30)
message = HumanMessage(
    content=[
        {"type": "text", "text": "describe the weather in this image"},
        {"type": "image_url", "image_url": {"url": image_url}},
    ],
)
response = model.invoke([message])
print(response.content)
# The weather in the image appears to be clear and sunny. The sky is mostly blue with a few scattered, light clouds. The sunlight is bright, casting clear shadows and illuminating the green grass and plants along the pathway. It looks like a pleasant day with good visibility and no signs of precipitation.


### 3. 여러 이미지 입력
print('-'*30)
message = HumanMessage(
    content=[
        {"type": "text", "text": "are these two images the same?"},
        {"type": "image_url", "image_url": {"url": image_url}},
        {"type": "image_url", "image_url": {"url": image_url}},
    ],
)
response = model.invoke([message])
print(response.content)
# Yes, the two images are the same. They both depict a wooden pathway leading through a grassy field under a blue sky with scattered clouds. The composition, colors, and details are identical in both images.