from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo").bind(logprobs=True)

msg = llm.invoke(("human", "how are you today"))

resuots = msg.response_metadata["logprobs"]["content"][:5]
print(resuots)
# [{'token': 'I', 'bytes': [73], 'logprob': -0.22784467, 'top_logprobs': []}, {'token': "'m", 'bytes': [39, 109], 'logprob': -0.32643092, 'top_logprobs': []}, {'token': ' an', 'bytes': [32, 97, 110], 'logprob': -2.2631042, 'top_logprobs': []}, {'token': ' AI', 'bytes': [32, 65, 73], 'logprob': -0.018693678, 'top_logprobs': []}, {'token': ',', 'bytes': [44], 'logprob': -1.3015928, 'top_logprobs': []}]