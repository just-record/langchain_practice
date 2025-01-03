from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


#################################################################################
### 1. Outpur parser를 사용 할 때 오류 발생 
### 출력에 문제가 있는 경우: 형식이 틀렸거나 내용이 부족한 경우
print('1.', '-' * 50)
##################################################################################
from langchain.output_parsers import OutputFixingParser
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from pydantic import BaseModel, Field


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
### prompt_value ###
rprint(prompt_value)
# 1. --------------------------------------------------
# StringPromptValue(
#     text='Answer the user query.\nThe output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of 
# strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}\nthe object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not 
# well-formatted.\n\nHere is the output schema:\n```\n{"properties": {"action": {"description": "action to take", "title": "Action", "type": "string"}, "action_input": {"description": "input to the action", "title": "Action 
# Input", "type": "string"}}, "required": ["action", "action_input"]}\n```\nwho is leo di caprios gf?\n'
# )


### 출력이 잘못된 경우를 설정 ###
bad_response = '{"action": "search"}'

print('')
try:
    parser.parse(bad_response)
    # parser.invoke(bad_response) ### 이것도 테스트 가능
except OutputParserException as e:
    print(e)
# Failed to parse Action from completion {"action": "search"}. Got: 1 validation error for Action
# action_input
#   Field required [type=missing, input_value={'action': 'search'}, input_type=dict]
#     For further information visit https://errors.pydantic.dev/2.10/v/missing
# For troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE     


#################################################################################
### 2. OutputFixingParser 로 오류를 수정
### 하지만 실질적으로 'action input'에 어떤 값을 넣어야 할지 알 수 없으므로 근본적인 문제가 해결이 안 됨
print('2.', '-' * 50)
##################################################################################
fix_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())
rprint(fix_parser.parse(bad_response))
# 2. --------------------------------------------------
# Action(action='search', action_input='keyword')
### action_input이 keyword로 설정되었지만, 이것은 임의로 설정한 값이므로 실제로는 잘못된 값


#################################################################################
### 3. RetryOutputParser 를 사용하여 원본 출력을 다시 가져오기
###  더 나은 응답을 얻기 위해 프롬프트와 원래 출력를 다시 전달하여 재시도
print('3.', '-' * 50)
##################################################################################
from langchain.output_parsers import RetryOutputParser

retry_parser = RetryOutputParser.from_llm(parser=parser, llm=OpenAI(temperature=0))
rprint(retry_parser.parse_with_prompt(bad_response, prompt_value))
# 3. --------------------------------------------------
# Action(action='search', action_input='leo di caprio girlfriend')


#################################################################################
### 4. RetryOutputParser 를 chaining 하기
###  더 나은 응답을 얻기 위해 프롬프트와 원래 출력를 다시 전달하여 재시도
print('4.', '-' * 50)
##################################################################################
from langchain_core.runnables import RunnableLambda, RunnableParallel

completion_chain = prompt | OpenAI(temperature=0)

main_chain = RunnableParallel(
    completion=completion_chain, prompt_value=prompt
) | RunnableLambda(lambda x: retry_parser.parse_with_prompt(**x))


rprint(main_chain.invoke({"query": "who is leo di caprios gf?"}))
# 4. --------------------------------------------------
# Action(action='search', action_input='leo di caprios gf')