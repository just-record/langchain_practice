from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnableConfig
from langchain_community.callbacks import get_openai_callback
from langchain_core.output_parsers import StrOutputParser

import json

def parse_or_fix(text: str, config: RunnableConfig):
    print(f'config: {config}')
    fixing_chain = (
        ChatPromptTemplate.from_template(
            "Fix the following text:\n\n```text\n{input}\n```\nError: {error}"
            " Don't narrate, just respond with the fixed data."
        )
        | model
        | StrOutputParser()
    )
    for _ in range(3):
        try:
            print(f'text(try): {text}')
            return json.loads(text)
        except Exception as e:
            print(f'text(except): {text}')
            print(f"Error: {e}")
            text = fixing_chain.invoke({"input": text, "error": e}, config)
    return "Failed to parse"

model = ChatOpenAI()

with get_openai_callback() as cb:
    output = RunnableLambda(parse_or_fix).invoke(
        "{foo: bar}", {"tags": ["my-tag"], "callbacks": [cb]}
    )
    print(f'output: {output}')
    print('-'*50)
    print(f'cb: {cb}')