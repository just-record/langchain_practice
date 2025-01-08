# 도구를 에이전트와 함께 사용할 때는 에러 처리 전략이 필요할 것입니다. 이를 통해 에이전트가 오류로부터 복구하고 실행을 계속할 수 있습니다.
# 간단한 전략은 도구 내부에서 ToolException을 발생시키고 handle_tool_error를 사용하여 오류 처리기를 지정하는 것입니다.
# 오류 처리기가 지정되면, 예외가 포착되고 오류 처리기가 도구에서 반환할 출력을 결정하게 됩니다.
# handle_tool_error를 True, 문자열 값 또는 함수로 설정할 수 있습니다. 함수인 경우, 해당 함수는 ToolException을 매개변수로 받아 값을 반환해야 합니다.
# ToolException만 발생시키는 것으로는 충분하지 않다는 점을 주의하세요. 도구의 handle_tool_error의 기본값이 False이므로, 먼저 이를 설정해야 합니다.

from rich import print as rprint
from langchain_core.tools import ToolException, StructuredTool


### 도구에서 ToolException 발생
def get_weather(city: str) -> int:
    """Get weather for the given city."""
    raise ToolException(f"Error: There is no city by the name of {city}.")


#################################################################################
### 1. 'handle_tool_error'를 사용 하지 않고 => 에러 발생
print('1.', '-' * 50)
################################################################################## 
get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    # handle_tool_error=True,
)

try:
    rprint(get_weather_tool.invoke({"city": "foobar"}))
except Exception:
    rprint("There is no city by the name of foobar.")
# 3. --------------------------------------------------
# There is no city by the name of foobar.    


#################################################################################
### 2. 'handle_tool_error' => True로 설정
print('2.', '-' * 50)
################################################################################## 
get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error=True,
)

rprint(get_weather_tool.invoke({"city": "foobar"}))
# 2. --------------------------------------------------
# Error: There is no city by the name of foobar.


#################################################################################
### 3. 'handle_tool_error' => string로 설정 -> 항상 string 값이 반환
print('3.', '-' * 50)
################################################################################## 
get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error="There is no such city, but it's probably above 0K there!",
)

rprint(get_weather_tool.invoke({"city": "foobar"}))
# 3. --------------------------------------------------
# There is no such city, but it's probably above 0K there!


#################################################################################
### 4. 'handle_tool_error' => 함수로 설정
print('4.', '-' * 50)
################################################################################## 
def _handle_error(error: ToolException) -> str:
    return f"The following errors occurred during tool execution: `{error.args[0]}`"


get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error=_handle_error,
)

rprint(get_weather_tool.invoke({"city": "foobar"}))
# 4. --------------------------------------------------
# The following errors occurred during tool execution: `Error: There is no city by the name of foobar.`