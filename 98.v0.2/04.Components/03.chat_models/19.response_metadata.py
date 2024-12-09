from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
msg = llm.invoke([("human", "What's the oldest known example of cuneiform")])
print(msg.response_metadata)
# {'token_usage': {'completion_tokens': 115, 'prompt_tokens': 16, 'total_tokens': 131}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_4008e3b719', 'finish_reason': 'stop', 'logprobs': None}