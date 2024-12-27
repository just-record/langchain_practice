from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("{foo}{bar}")


#################################################################################
### 1. partial() 사용하여 문자열을 부분 포맷팅
print('1.', '-' * 50)
##################################################################################
partial_prompt = prompt.partial(foo="foo")
print(partial_prompt)
# 1. --------------------------------------------------
# input_variables=['bar'] input_types={} partial_variables={'foo': 'foo'} template='{foo}{bar}'

print(' ')
print(partial_prompt.format(bar="baz"))
# foobaz


#################################################################################
### 2. partial_variables 을 사용하여 문자열을 부분 포맷팅
print('2.', '-' * 50)
##################################################################################
prompt = PromptTemplate(
    template="{foo}{bar}", input_variables=["bar"], partial_variables={"foo": "foo"}
)
print(prompt.format(bar="baz"))
# 2. --------------------------------------------------
# foobaz


#################################################################################
### 3. partial() 사용하여 함수를 부분 포맷팅
print('3.', '-' * 50)
##################################################################################
from datetime import datetime


def _get_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")


prompt = PromptTemplate(
    template="Tell me a {adjective} joke about the day {date}",
    input_variables=["adjective", "date"],
)
partial_prompt = prompt.partial(date=_get_datetime)
print(partial_prompt)
# 3. --------------------------------------------------
# input_variables=['adjective'] input_types={} partial_variables={'date': <function _get_datetime at 0x78d522d23d90>} template='Tell me a {adjective} joke about the day {date}'

print(' ')
print(partial_prompt.format(adjective="funny"))
# Tell me a funny joke about the day 12/27/2024, 13:53:10


#################################################################################
### 4. partial_variables 을 사용하여 함수를 부분 포맷팅
print('4.', '-' * 50)
##################################################################################
prompt = PromptTemplate(
    template="Tell me a {adjective} joke about the day {date}",
    input_variables=["adjective"],
    partial_variables={"date": _get_datetime},
)
print(prompt.format(adjective="funny"))
# 4. --------------------------------------------------
# Tell me a funny joke about the day 12/27/2024, 13:54:12