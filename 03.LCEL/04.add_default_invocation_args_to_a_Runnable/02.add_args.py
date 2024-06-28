from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Write out the following equation using algebraic symbols then solve it. Use the format\n\nEQUATION:...\nSOLUTION:...\n\n",
        ),
        ("human", "{equation_statement}"),
    ]
)

model = ChatOpenAI(temperature=0)

runnable = (
    {"equation_statement": RunnablePassthrough()}
    | prompt
    ### stop word를 상수 인수로 설정 하여 모델에 바인딩
    | model.bind(stop="SOLUTION")  # 다른 예시: max_tokens=10   등...
    | StrOutputParser()
)

print(runnable.invoke("x raised to the third plus seven equals 12"))

### 출력
# EQUATION: x^3 + 7 = 12
#
#

