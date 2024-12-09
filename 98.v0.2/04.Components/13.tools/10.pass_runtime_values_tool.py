from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

### 1. Passing request time information
# 요청 시점에 동적으로 tool을 생성 하고 요청에 포함된 사용자 ID을 tool에 전달
from typing import List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.tools import BaseTool, tool

user_to_pets = {}


def generate_tools_for_user(user_id: str) -> List[BaseTool]:
    """Generate a set of tools that have a user id associated with them."""

    @tool
    def update_favorite_pets(pets: List[str]) -> None:
        """Add the list of favorite pets."""
        user_to_pets[user_id] = pets

    @tool
    def delete_favorite_pets() -> None:
        """Delete the list of favorite pets."""
        if user_id in user_to_pets:
            del user_to_pets[user_id]

    @tool
    def list_favorite_pets() -> None:
        """List favorite pets if any."""
        return user_to_pets.get(user_id, [])

    return [update_favorite_pets, delete_favorite_pets, list_favorite_pets]

# tool이 제대로 작동 하는지 확인
update_pets, delete_pets, list_pets = generate_tools_for_user("eugene")
update_pets.invoke({"pets": ["cat", "dog"]})
print(user_to_pets) # {'eugene': ['cat', 'dog']}
print(list_pets.invoke({})) # ['cat', 'dog']


# LLM은 사용자 ID를 알지 못한체 tool을 호출
print('-'*30)
from langchain_core.prompts import ChatPromptTemplate


def handle_run_time_request(user_id: str, query: str):
    """Handle run time request."""
    tools = generate_tools_for_user(user_id)
    llm_with_tools = llm.bind_tools(tools)
    prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant.")],
    )
    chain = prompt | llm_with_tools
    return llm_with_tools.invoke(query)


ai_message = handle_run_time_request(
    "eugene", "my favorite animals are cats and parrots."
)
print(ai_message.tool_calls)
# [{'name': 'update_favorite_pets', 'args': {'pets': ['cats', 'parrots']}, 'id': 'call_QNHyoFAHuvvlupV2lVX1ifLW'}]

# 다른 사용자 계정
print('-'*30)
ai_message2 = handle_run_time_request(
    "hong", "my favorite animals are dogs and cats"
)
print(ai_message2.tool_calls)
# [{'name': 'update_favorite_pets', 'args': {'pets': ['dogs', 'cats']}, 'id': 'call_8Kk7OUTQc0emwQmbIJu8lALJ'}]
