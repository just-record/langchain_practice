from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model

### 1. 기본 사용법
# Returns a langchain_openai.ChatOpenAI instance.
gpt_4o = init_chat_model("gpt-4o", model_provider="openai", temperature=0)
# Returns a langchain_anthropic.ChatAnthropic instance.
claude_opus = init_chat_model(
    "claude-3-opus-20240229", model_provider="anthropic", temperature=0
)
### 'pip install -U langchain-google-vertexai' 필요 - 일단 생략 - 어차피 key가 없어서 실행이 안됨
# Returns a langchain_google_vertexai.ChatVertexAI instance.
# gemini_15 = init_chat_model(
#     "gemini-1.5-pro", model_provider="google_vertexai", temperature=0
# )

# Since all model integrations implement the ChatModel interface, you can use them in the same way.
### 인증키가 없어서 OpenAI만 확인 함
print("GPT-4o: " + gpt_4o.invoke("what's your name").content + "\n")
# print("Claude Opus: " + claude_opus.invoke("what's your name").content + "\n")
# print("Gemini 1.5: " + gemini_15.invoke("what's your name").content + "\n")


### 2. 설정하기
print('-'*30)
user_config = {
    "model": "gpt-4o",
    "model_provider": "openai",
    "temperature": 0,
    "max_tokens": 1000,
}

llm = init_chat_model(**user_config)
results = llm.invoke("what's your name")
print(results.content)
# I'm an AI language model created by OpenAI, and I don't have a personal name. You can call me Assistant or any other name you prefer! How can I assist you today?


### 3. model provider 추론하기
print('-'*30)
gpt_4o = init_chat_model("gpt-4o", temperature=0)
claude_opus = init_chat_model("claude-3-opus-20240229", temperature=0)
# gemini_15 = init_chat_model("gemini-1.5-pro", temperature=0)
print(f'gpt_4o: {gpt_4o}')
print(f'claude_opus: {claude_opus}')
# print(f'gemini_15: {gemini_15}')