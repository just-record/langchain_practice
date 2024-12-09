from dotenv import load_dotenv
load_dotenv()

from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI, OpenAI

template = """Based on the user question, provide an Action and Action Input for what step should be taken.
{format_instructions}
Question: {query}
Response:"""


class Action(BaseModel):
    action: str = Field(description="action to take")
    action_input: str = Field(description="input to the action")


parser = PydanticOutputParser(pydantic_object=Action)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

prompt_value = prompt.format_prompt(query="who is leo di caprios gf?")

bad_response = '{"action": "search"}'

### 1. 잘못 된 결과값으로 인해 parsing시 에러 발생
try:
    parser.parse(bad_response)
except Exception as e:
    print(f'Error: {e}')
# Error: Failed to parse Action from completion {"action": "search"}. Got: 1 validation error for Action
# action_input
#   field required (type=value_error.missing)    

### 2. OutputFixingParser를 사용하여 오류를 수정? => 'action input'에 어떤 값을 넣어야 하는지 알 수 없음.

# print('-'*30)
# fix_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())
# print(fix_parser.parse(bad_response))


### 3. RetryOutputParser를 사용 하여 질의를 다시 시도
### 공식 예제는 있으나 오류가 발생함. -> 아직 완전히 이해 하지 못 한 듯
# print('-'*30)
# from langchain.output_parsers import RetryOutputParser
# retry_parser = RetryOutputParser.from_llm(parser=parser, llm=OpenAI(temperature=0))
# print(retry_parser.parse_with_prompt(bad_response, prompt_value))


### 4. chain을 사용 하여 RetryOutputParser를 사용
print('-'*30)
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain.output_parsers import RetryOutputParser

retry_parser = RetryOutputParser.from_llm(parser=parser, llm=OpenAI(temperature=0))

completion_chain = prompt | OpenAI(temperature=0)

main_chain = RunnableParallel(
    completion=completion_chain, 
    prompt_value=prompt
) | RunnableLambda(lambda x: retry_parser.parse_with_prompt(**x))
## RunnableParallel에 의해 아래 값 전달
# {
#     'completion': [모델의 응답],
#     'prompt_value': [원본 프롬프트]
# }
## retry_parser: 파싱에 성공 하면 결과를 반환, 파싱에 실패하면 
# - 오류 메시지를 생성합니다.
# - 원본 프롬프트, 이전 응답, 그리고 오류 메시지를 포함한 새로운 프롬프트를 만듭니다.
# - 이 새 프롬프트로 LLM에 다시 쿼리를 보냅니다.
# - 새로운 응답을 받아 다시 파싱을 시도합니다.
# 재시도 횟수까지 반복
retry_cnt = 0
try:
    results = main_chain.invoke({"query": "who is leo di caprios gf?"})
    print(results)
    # action='search' action_input='leo di caprios gf'
except Exception as e:
    print(f'retry_cnt: {retry_cnt}, Error: {e}')
    retry_cnt += 1
