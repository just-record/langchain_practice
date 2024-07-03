from langchain_core.prompts import PromptTemplate
from datetime import datetime


def _get_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")


### 부분을 포매팅 하기(함수) - 방법 1
prompt = PromptTemplate(
    template="Tell me a {adjective} joke about the day {date}",
    input_variables=["adjective", "date"],
)
partial_prompt = prompt.partial(date=_get_datetime)
print(partial_prompt.format(adjective="funny"))
# Tell me a funny joke about the day 07/03/2024, 19:30:23


### 부분을 포매팅 하기(함수) - 방법 2
print("-" * 30)
prompt = PromptTemplate(
    template="Tell me a {adjective} joke about the day {date}",
    input_variables=["adjective"],
    partial_variables={"date": _get_datetime},
)
print(prompt.format(adjective="funny"))
# Tell me a funny joke about the day 07/03/2024, 19:30:23


### 이것도 되긴 되네
print("-" * 30)
prompt = PromptTemplate(
    template="Tell me a {adjective} joke about the day {date}",
    input_variables=["adjective", "date"],
)
print(prompt.format(adjective="funny", date=_get_datetime()))
