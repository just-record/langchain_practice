from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import base64
import httpx

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")

model = ChatOpenAI(model="gpt-4o")


### 1. prompts
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

chain = prompt | model
response = chain.invoke({"image_data": image_data})
print(response.content)
# The image depicts a serene landscape with a wooden boardwalk leading through a lush, green meadow. The sky above is mostly clear, with a few scattered clouds, and it is painted in shades of blue and white. In the background, there are trees and shrubs, adding to the tranquil and natural atmosphere of the scene. The boardwalk seems to stretch into the distance, inviting viewers to follow it and explore the peaceful surroundings. The bright, vibrant colors suggest a sunny day, possibly in spring or summer.


### 2. prompts - multiple images
print('-'*30)
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
print(response.content)
# The two images provided are identical. Both depict a wooden walkway through a grassy field with a clear blue sky and scattered clouds. The landscape includes green grasses, bushes, and distant trees. The angle, lighting, and composition are the same in both images.