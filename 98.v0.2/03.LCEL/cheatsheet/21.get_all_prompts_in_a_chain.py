from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel

prompt1 = ChatPromptTemplate.from_messages(
    [("system", "good ai"), ("human", "{input}")]
)
prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system", "really good ai"),
        ("human", "{input}"),
        ("ai", "{ai_output}"),
        ("human", "{input2}"),
    ]
)

fake_llm = RunnableLambda(lambda prompt: "i am good ai")

# 수정된 체인
chain = (
    RunnableParallel(
        {
            "input": RunnablePassthrough(),
            "ai_output": prompt1 | fake_llm,
            "input2": lambda x: x["input2"]  # input2를 전달
        }
    )
    | prompt2
    | fake_llm
)

# 체인 실행 (input2 포함)
result = chain.invoke({"input": "hi", "input2": "how are you?"})
print(result)
# i am good ai


# get_prompts
print("-" * 30)
for i, prompt in enumerate(chain.get_prompts()):
    print(f"**prompt {i=}**\n")
    print(prompt.pretty_repr())
    print("\n" * 3)