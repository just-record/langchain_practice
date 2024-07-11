from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate


class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"----- My custom handler -----, token: {token}")


prompt = ChatPromptTemplate.from_messages(["Tell me a joke about {animal}"])

# To enable streaming, we pass in `streaming=True` to the ChatModel constructor
# Additionally, we pass in our custom handler as a list to the callbacks parameter
model = ChatAnthropic(
    model="claude-3-sonnet-20240229", streaming=True, callbacks=[MyCustomHandler()]
)

chain = prompt | model

response = chain.invoke({"animal": "bears"})
print(response)
# ----- My custom handler -----, token: 
# ----- My custom handler -----, token: Here's a bear
# ----- My custom handler -----, token:  joke
# ----- My custom handler -----, token:  for
# ----- My custom handler -----, token:  you:

# Why
# ----- My custom handler -----, token:  di
# ----- My custom handler -----, token: d the bear dissol
# ----- My custom handler -----, token: ve in
# ----- My custom handler -----, token:  water
# ----- My custom handler -----, token: ?
# ----- My custom handler -----, token: 
# Because it was
# ----- My custom handler -----, token:  a polar
# ----- My custom handler -----, token:  bear!
# ----- My custom handler -----, token: 
# content="Here's a bear joke for you:\n\nWhy did the bear dissolve in water?\nBecause it was a polar bear!" id='run-33cc795f-72e9-438f-9c35-ea1911365a49-0' usage_metadata={'input_tokens': 13, 'output_tokens': 30, 'total_tokens': 43}