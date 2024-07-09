from langchain_core.tools import ToolException
from langchain_core.tools import StructuredTool


### error를 발생 - 'ToolException'를 사용
def get_weather(city: str) -> int:
    """Get weather for the given city."""
    raise ToolException(f"Error: There is no city by the name of {city}.")


### handle_tool_error=True 로 설정 하여 error를 처리하도록 함
get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error=True,   # True로 설정 하여 error를 처리하도록 함
)


### 1. error 발생 되는 tool 호출
print(get_weather_tool.invoke({"city": "foobar"}))
# Error: There is no city by the name of foobar.


### 2. 'handle_tool_error'를 문자열로 설정
print('-'*30)
get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error="There is no such city, but it's probably above 0K there!",
)

print(get_weather_tool.invoke({"city": "foobar"}))
# There is no such city, but it's probably above 0K there!


### 3. 'handle_tool_error'를 함수로 설정
print('-'*30)
def _handle_error(error: ToolException) -> str:
    return f"The following errors occurred during tool execution: `{error.args[0]}`"


get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error=_handle_error,
)

print(get_weather_tool.invoke({"city": "foobar"}))
# The following errors occurred during tool execution: `Error: There is no city by the name of foobar.`