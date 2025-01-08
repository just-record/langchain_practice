# run time에만 알 수 있는 값들을 도구에 바인딩해야 할 수 있습니다.(ex: 사용자의 ID)
# 대부분의 경우, 이러한 값들은 LLM이 제어해서는 안 됩니다. 실제로 LLM이 사용자 ID를 제어할 수 있도록 허용하면 보안 위험이 발생할 수 있습니다.
# 대신, LLM은 LLM이 제어하도록 설계된 도구의 매개변수만 제어해야 하며, 다른 매개변수(사용자 ID 등)는 애플리케이션 로직에 의해 고정되어야 합니다.

from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
from typing import List
from langchain_core.tools import InjectedToolArg, tool
from typing_extensions import Annotated

llm = ChatOpenAI(model="gpt-4o-mini")

user_to_pets = {}


@tool(parse_docstring=True)
def update_favorite_pets(
    pets: List[str], user_id: Annotated[str, InjectedToolArg]
) -> None:
    """Add the list of favorite pets.

    Args:
        pets: List of favorite pets to set.
        user_id: User's ID.
    """
    user_to_pets[user_id] = pets


@tool(parse_docstring=True)
def delete_favorite_pets(user_id: Annotated[str, InjectedToolArg]) -> None:
    """Delete the list of favorite pets.

    Args:
        user_id: User's ID.
    """
    if user_id in user_to_pets:
        del user_to_pets[user_id]


@tool(parse_docstring=True)
def list_favorite_pets(user_id: Annotated[str, InjectedToolArg]) -> None:
    """List favorite pets if any.

    Args:
        user_id: User's ID.
    """
    return user_to_pets.get(user_id, [])


#################################################################################
### 1. Hiding arguments from the model
### Tool의 특정 매개변수(예: user_id)를 InjectedToolArg 어노테이션으로 표시하여 런타임에 주입
### 해당 매개변수가 모델에 의해 생성되지 않아야 함
# print('1.', '-' * 50)
################################################################################## 

#################################################################################
### 1-1. input schemas 보기 - user_id가 존재
print('1-1.', '-' * 50)
################################################################################## 
# rprint(update_favorite_pets.get_input_schema().schema()) schema() ==> model_json_schema()
rprint(update_favorite_pets.get_input_schema().model_json_schema())
# 1-1. --------------------------------------------------
# {
#     'description': 'Add the list of favorite pets.',
#     'properties': {
#         'pets': {'description': 'List of favorite pets to set.', 'items': {'type': 'string'}, 'title': 'Pets', 'type': 'array'},
#         'user_id': {'description': "User's ID.", 'title': 'User Id', 'type': 'string'}
#     },
#     'required': ['pets', 'user_id'],
#     'title': 'update_favorite_pets',
#     'type': 'object'
# }


#################################################################################
### 1-2. tool schemas 보기 - too calling를 위해 모델에 전달된 schema - user_id가 없음
### InjectedToolArg
print('1-2.', '-' * 50)
################################################################################## 
rprint(update_favorite_pets.tool_call_schema.model_json_schema())
# 1-2. --------------------------------------------------
# {
#     'description': 'Add the list of favorite pets.',
#     'properties': {'pets': {'description': 'List of favorite pets to set.', 'items': {'type': 'string'}, 'title': 'Pets', 'type': 'array'}},
#     'required': ['pets'],
#     'title': 'update_favorite_pets',
#     'type': 'object'
# }


#################################################################################
### 1-3. tool을 invoke할 때 user_id를 전달 해야 함
print('1-3.', '-' * 50)
################################################################################## 
user_id = "123"
update_favorite_pets.invoke({"pets": ["lizard", "dog"], "user_id": user_id})
rprint(user_to_pets)
rprint(list_favorite_pets.invoke({"user_id": user_id}))
# 1-3. --------------------------------------------------
# {'123': ['lizard', 'dog']}
# ['lizard', 'dog']


#################################################################################
### 1-4. model이 tool을 호출할 때 user_id는 생성하지 않음
print('1-4.', '-' * 50)
################################################################################## 
tools = [
    update_favorite_pets,
    delete_favorite_pets,
    list_favorite_pets,
]
llm_with_tools = llm.bind_tools(tools)
ai_msg = llm_with_tools.invoke("my favorite animals are cats and parrots")
rprint(ai_msg.tool_calls)
# 1-4. --------------------------------------------------
# [{'name': 'update_favorite_pets', 'args': {'pets': ['cats', 'parrots']}, 'id': 'call_8Vssb0pWoKBNlhTAYxgw1lkZ', 'type': 'tool_call'}]


#################################################################################
### 2. Injecting arguments at runtime
# print('2.', '-' * 50)
################################################################################## 
from copy import deepcopy

from langchain_core.runnables import chain


#################################################################################
### 2-1. user_id를 inject 하기
print('2-1.', '-' * 50)
################################################################################## 
@chain
def inject_user_id(ai_msg):
    tool_calls = []
    for tool_call in ai_msg.tool_calls:
        tool_call_copy = deepcopy(tool_call)
        tool_call_copy["args"]["user_id"] = user_id
        tool_calls.append(tool_call_copy)
    return tool_calls

rprint(inject_user_id.invoke(ai_msg))


#################################################################################
### 2-2. 모델과 injection code와 실제 tool을 chaining 하기 
print('2-2.', '-' * 50)
################################################################################## 
tool_map = {tool.name: tool for tool in tools}


@chain
def tool_router(tool_call):
    return tool_map[tool_call["name"]]


chain = llm_with_tools | inject_user_id | tool_router.map()
rprint(chain.invoke("my favorite animals are cats and parrots"))
# 2-2. --------------------------------------------------
# [ToolMessage(content='null', name='update_favorite_pets', tool_call_id='call_1bfQH2bSyRJIeKtX5qiWMkO2')]


#################################################################################
### 2-3. user_to_pets
print('2-3.', '-' * 50)
################################################################################## 
rprint(user_to_pets)
# 2-3. --------------------------------------------------
# {'123': ['cats', 'parrots']}


#################################################################################
### 3. Other ways of annotating args
# print('3.', '-' * 50)
################################################################################## 

#################################################################################
### 3-1. BaseModel을 상속받아서 schema 구현 - input schema 확인
### user_id를 InjectedToolArg로 Annotated으로 표시
print('3-1.', '-' * 50)
################################################################################## 
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class UpdateFavoritePetsSchema(BaseModel):
    """Update list of favorite pets"""

    pets: List[str] = Field(..., description="List of favorite pets to set.")
    user_id: Annotated[str, InjectedToolArg] = Field(..., description="User's ID.")


@tool(args_schema=UpdateFavoritePetsSchema)
def update_favorite_pets(pets, user_id):
    user_to_pets[user_id] = pets


rprint(update_favorite_pets.get_input_schema().model_json_schema())
# 3-1. --------------------------------------------------
# {
#     'description': 'Update list of favorite pets',
#     'properties': {
#         'pets': {'description': 'List of favorite pets to set.', 'items': {'type': 'string'}, 'title': 'Pets', 'type': 'array'},
#         'user_id': {'description': "User's ID.", 'title': 'User Id', 'type': 'string'}
#     },
#     'required': ['pets', 'user_id'],
#     'title': 'UpdateFavoritePetsSchema',
#     'type': 'object'
# }


#################################################################################
### 3-2. tool_call_schema 확인
### user_id는 tool_call_schema에 없음 -> 모델이 user_id를 생성하지 않음
print('3-2.', '-' * 50)
################################################################################## 
rprint(update_favorite_pets.tool_call_schema.model_json_schema())
# 3-2. --------------------------------------------------
# {
#     'description': 'Update list of favorite pets',
#     'properties': {'pets': {'description': 'List of favorite pets to set.', 'items': {'type': 'string'}, 'title': 'Pets', 'type': 'array'}},
#     'required': ['pets'],
#     'title': 'update_favorite_pets',
#     'type': 'object'
# }


#################################################################################
### 3-3. BaseTool을 상속받아서 tool 구현 - input schema 확인
### tool이 어서 user_id가 존재 함
print('3-3.', '-' * 50)
################################################################################## 
from typing import Optional, Type


class UpdateFavoritePets(BaseTool):
    name: str = "update_favorite_pets"
    description: str = "Update list of favorite pets"
    args_schema: Optional[Type[BaseModel]] = UpdateFavoritePetsSchema

    def _run(self, pets, user_id):
        user_to_pets[user_id] = pets


rprint(UpdateFavoritePets().get_input_schema().model_json_schema())
# 3-3. --------------------------------------------------
# {
#     'description': 'Update list of favorite pets',
#     'properties': {
#         'pets': {'description': 'List of favorite pets to set.', 'items': {'type': 'string'}, 'title': 'Pets', 'type': 'array'},
#         'user_id': {'description': "User's ID.", 'title': 'User Id', 'type': 'string'}
#     },
#     'required': ['pets', 'user_id'],
#     'title': 'UpdateFavoritePetsSchema',
#     'type': 'object'
# }


#################################################################################
### 3-4. tool의 tool_call_schema 확인
### user_id는 tool_call_schema에 없음 -> 모델이 user_id를 생성하지 않음
print('3-4.', '-' * 50)
################################################################################## 
rprint(UpdateFavoritePets().tool_call_schema.model_json_schema())
# 3-4. --------------------------------------------------
# {
#     'description': 'Update list of favorite pets',
#     'properties': {'pets': {'description': 'List of favorite pets to set.', 'items': {'type': 'string'}, 'title': 'Pets', 'type': 'array'}},
#     'required': ['pets'],
#     'title': 'update_favorite_pets',
#     'type': 'object'
# }

print(' ')
UpdateFavoritePets().invoke({"pets": ["lizard", "dog"], "user_id": "456"})
rprint(user_to_pets)
# {'123': ['cats', 'parrots'], '456': ['lizard', 'dog']}

#################################################################################
### 3-5. tool을 만드는 다른 방법
### BaseTool을 상속받아서 UpdateFavoritePets2 구현 - input schema 확인
### 속성에 user_id를 정의 하지 않음, _run() 의 parameter에 user_id를 정의(InjectedToolArg)
### input schema에 user_id가 없음
print('3-5.', '-' * 50)
################################################################################## 
class UpdateFavoritePets2(BaseTool):
    name: str = "update_favorite_pets"
    description: str = "Update list of favorite pets"

    def _run(self, pets: List[str], user_id: Annotated[str, InjectedToolArg]) -> None:
        user_to_pets[user_id] = pets


rprint(UpdateFavoritePets2().get_input_schema().model_json_schema())

# 3-5. --------------------------------------------------
# {
#     'description': 'Use the tool.\n\nAdd run_manager: Optional[CallbackManagerForToolRun] = None\nto child implementations to enable tracing.',
#     'properties': {'pets': {'items': {'type': 'string'}, 'title': 'Pets', 'type': 'array'}, 'user_id': {'title': 'User Id', 'type': 'string'}},
#     'required': ['pets', 'user_id'],
#     'title': 'update_favorite_pets',
#     'type': 'object'
# }

#################################################################################
### 3-6. tool_call_schema 확인
print('3-6.', '-' * 50)
################################################################################## 
rprint(UpdateFavoritePets2().tool_call_schema.model_json_schema())
# 3-6. --------------------------------------------------
# {'description': 'Update list of favorite pets', 'properties': {'pets': {'items': {'type': 'string'}, 'title': 'Pets', 'type': 'array'}}, 'required': ['pets'], 'title': 'update_favorite_pets', 'type': 'object'}

print(' ')
UpdateFavoritePets2().invoke({"pets": ["lizard", "dog"], "user_id": "456"})
rprint(user_to_pets)
# {'123': ['cats', 'parrots'], '456': ['lizard', 'dog']}