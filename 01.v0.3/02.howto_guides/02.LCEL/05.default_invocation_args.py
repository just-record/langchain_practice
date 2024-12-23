from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


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
    {"equation_statement": RunnablePassthrough()} | prompt | model | StrOutputParser()
)


##################################################################################
### 1. 간단한 prompt와 model 체인
print('1.', '-' * 50)
##################################################################################

print(runnable.invoke("x raised to the third plus seven equals 12"))
# 1. --------------------------------------------------
# EQUATION: x^3 + 7 = 12

# SOLUTION: 
# Subtract 7 from both sides:
# x^3 = 5

# Take the cube root of both sides:
# x = ∛5


##################################################################################
### 2. .bind()를 사용하여 Runnable의 상수 인자 설정
# stop 인자를 "SOLUTION"으로 설정하면 Runnable은 "SOLUTION"이라는 문자열을 만나면 정지 함
print('2.', '-' * 50)
##################################################################################
runnable = (
    {"equation_statement": RunnablePassthrough()}
    | prompt
    | model.bind(stop="SOLUTION")
    | StrOutputParser()
)

print(runnable.invoke("x raised to the third plus seven equals 12"))
# 2. --------------------------------------------------
# EQUATION: x^3 + 7 = 12

