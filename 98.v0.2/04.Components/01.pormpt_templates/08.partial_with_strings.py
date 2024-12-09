from langchain_core.prompts import PromptTemplate

### 부분을 포매팅 하기(문자열) - 방법 1
prompt = PromptTemplate.from_template("{foo}{bar}")
partial_prompt = prompt.partial(foo="foo")
print(partial_prompt.format(bar="baz"))
# foobaz

### 부분을 포매팅 하기(문자열) - 방법 2
print('-'*30)
prompt = PromptTemplate(
    template="{foo}{bar}", input_variables=["bar"], partial_variables={"foo": "foo"}
)
print(prompt.format(bar="baz"))
# foobaz