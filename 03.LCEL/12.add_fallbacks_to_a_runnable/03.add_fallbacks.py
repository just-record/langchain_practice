from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a nice assistant who always includes a compliment in your response",
        ),
        ("human", "Why did the {animal} cross the road"),
    ]
)


# gpt-fake로 오류를 발생
# ChatOpenAI은 ChatPromptTemplate 사용
chat_model  = ChatOpenAI(model="gpt-fake")
bad_chain = chat_prompt | chat_model | StrOutputParser()


prompt_template = """Instructions: You should always include a compliment in your response.

Question: Why did the {animal} cross the road?"""

# OpenAI는 PromptTemplate 사용(ChatPromptTemplate X)
prompt = PromptTemplate.from_template(prompt_template)
llm = OpenAI()
good_chain = prompt | llm


# fallbacks 설정
chain = bad_chain.with_fallbacks([good_chain])

### fallbacks을 적용
try:
    print(chain.invoke({"animal": "turtle"}))
except Exception as e:
    print(f'Error: {e}')
# 출력: OpenAI 적용 됨. PromptTemplate이 사용 됨
# Response: That's a great question! I admire your curiosity and sense of humor. Well, I believe the turtle crossed the road because it wanted to explore the other side.
