from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic

# https://docs.anthropic.com/en/docs/about-claude/models
chat_model = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0.7,
    max_tokens=150,
)    

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of Korea?"}
]

result = chat_model.invoke(messages)
print(result.content)
# There are actually two countries commonly referred to as Korea:
# 1. South Korea (officially the Republic of Korea): The capital is Seoul.
# 2. North Korea (officially the Democratic People's Republic of Korea): The capital is Pyongyang.
# When people ask about "Korea" without specifying North or South, they are often referring to South Korea. In this case, the capital would be Seoul, which is also the largest city in South Korea and one of the largest metropolitan areas in the world.