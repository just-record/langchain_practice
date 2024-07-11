from dotenv import load_dotenv
load_dotenv()

from typing import Any, Dict, List

from langchain_anthropic import ChatAnthropic
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate


class LoggingHandler(BaseCallbackHandler):
    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
    ) -> None:
        print("----- Chat model started -----")

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        print(f"----- Chat model ended -----, response: {response}")

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs
    ) -> None:
        print(f"----- Chain {serialized.get('name')} started -----")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        print(f"----- Chain ended -----, outputs: {outputs}")


callbacks = [LoggingHandler()]
llm = ChatAnthropic(model="claude-3-sonnet-20240229")
prompt = ChatPromptTemplate.from_template("What is 1 + {number}?")

chain = prompt | llm

print(chain.invoke({"number": "2"}, config={"callbacks": callbacks}))
# ----- Chain RunnableSequence started -----
# ----- Chain ChatPromptTemplate started -----
# ----- Chain ended -----, outputs: messages=[HumanMessage(content='What is 1 + 2?')]
# ----- Chat model started -----
# ----- Chat model ended -----, response: generations=[[ChatGeneration(text='1 + 2 = 3', message=AIMessage(content='1 + 2 = 3', response_metadata={'id': 'msg_01R6gXiLp7Y7Ey8p8Dz7Z2Wy', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 16, 'output_tokens': 13}}, id='run-ac3f86fa-34e4-4cfe-aef6-4223a2ad2d9c-0', usage_metadata={'input_tokens': 16, 'output_tokens': 13, 'total_tokens': 29}))]] llm_output={'id': 'msg_01R6gXiLp7Y7Ey8p8Dz7Z2Wy', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 16, 'output_tokens': 13}} run=None
# ----- Chain ended -----, outputs: content='1 + 2 = 3' response_metadata={'id': 'msg_01R6gXiLp7Y7Ey8p8Dz7Z2Wy', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 16, 'output_tokens': 13}} id='run-ac3f86fa-34e4-4cfe-aef6-4223a2ad2d9c-0' usage_metadata={'input_tokens': 16, 'output_tokens': 13, 'total_tokens': 29}
# content='1 + 2 = 3' response_metadata={'id': 'msg_01R6gXiLp7Y7Ey8p8Dz7Z2Wy', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 16, 'output_tokens': 13}} id='run-ac3f86fa-34e4-4cfe-aef6-4223a2ad2d9c-0' usage_metadata={'input_tokens': 16, 'output_tokens': 13, 'total_tokens': 29}