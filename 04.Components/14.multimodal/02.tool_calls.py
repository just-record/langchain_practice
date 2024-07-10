from dotenv import load_dotenv
load_dotenv()

from typing import Literal

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool
def weather_tool(weather: Literal["sunny", "cloudy", "rainy"]) -> None:
    """Describe the weather"""
    pass


model = ChatOpenAI(model="gpt-4o")
model_with_tools = model.bind_tools([weather_tool])

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"

message = HumanMessage(
    content=[
        {"type": "text", "text": "describe the weather in this image"},
        {"type": "image_url", "image_url": {"url": image_url}},
    ],
)
response = model_with_tools.invoke([message])
print(response.tool_calls)
# [{'name': 'weather_tool', 'args': {'weather': 'sunny'}, 'id': 'call_y9yKQdc9DDVy7F5Q3PYQtboE'}]