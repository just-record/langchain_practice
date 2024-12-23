from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

##################################################################################
### 1. The pipe operator(|) 로 Runnable 개체 연결 하기
print('1.', '-' * 50)
##################################################################################
chain = prompt | model | StrOutputParser()
results = chain.invoke({"topic": "bears"})
rprint(results)
# 1. --------------------------------------------------
# Why do bears have hairy coats?

# Because they look silly in sweaters!


##################################################################################
### 2. 위의 chain을 다른 Runnable 개체와 연결 하기
print('2.', '-' * 50)
##################################################################################
from langchain_core.output_parsers import StrOutputParser

analysis_prompt = ChatPromptTemplate.from_template("is this a funny joke? {joke}")

composed_chain = {"joke": chain} | analysis_prompt | model | StrOutputParser()

results = composed_chain.invoke({"topic": "bears"})
rprint(results)
# 2. --------------------------------------------------
# Yes, that's a lighthearted and funny joke! It has a playful punchline that creates a humorous mental image of bears trying to wear sweaters. The silliness of the idea adds to the charm of the joke. Would you like to hear more 
# jokes or maybe some variations on this one?


##################################################################################
### 3. 위의 chain을 다른 Runnable 개체와 연결 하는 다른 방식
print('3.', '-' * 50)
##################################################################################
composed_chain_with_lambda = (
    chain
    | (lambda input: {"joke": input})
    | analysis_prompt
    | model
    | StrOutputParser()
)

results = composed_chain_with_lambda.invoke({"topic": "beets"})
rprint(results)
# 3. --------------------------------------------------
# That's a cute pun! The play on words with "root" makes it a light-hearted joke, especially for those who appreciate vegetable humor. It’s definitely funny in a wholesome, cheesy way!


##################################################################################
### 4. The .pipe() method 도 위의 '|' 연산자와 같은 역할
print('4.', '-' * 50)
##################################################################################
from langchain_core.runnables import RunnableParallel

composed_chain_with_pipe = (
    RunnableParallel({"joke": chain})
    .pipe(analysis_prompt)
    .pipe(model)
    .pipe(StrOutputParser())
)

results = composed_chain_with_pipe.invoke({"topic": "battlestar galactica"})
rprint(results)
# 4. --------------------------------------------------
# That's a clever joke, especially for fans of "Battlestar Galactica"! The play on words with "download" relates to both technology and emotions, making it a nice blend of sci-fi humor. If your audience appreciates that show, 
# they'll likely find it funny!


##################################################################################
### 5. The .pipe() method 의 다른 사용법
print('5.', '-' * 50)
##################################################################################
from langchain_core.runnables import RunnableLambda

composed_chain_with_pipe = (
    chain.pipe(lambda input: {"joke": input})
    .pipe(analysis_prompt)
    .pipe(model)
    .pipe(StrOutputParser())
)

results = composed_chain_with_pipe.invoke({"topic": "battlestar galactica"})
rprint(results)
# 5. --------------------------------------------------
# That's a clever joke, especially if the audience is familiar with "Battlestar Galactica" and its themes! The play on "unresolved issues" in the context of therapy and the relationship between Cylons and their creators adds a 
# nice touch of humor. If your audience appreciates sci-f


##################################################################################
### 6. The .pipe() method 의 다른 사용법 2
print('6.', '-' * 50)
##################################################################################
from langchain_core.runnables import RunnableLambda

composed_chain_with_pipe = RunnableParallel({"joke": chain}).pipe(
    analysis_prompt, model, StrOutputParser()
)

results = composed_chain_with_pipe.invoke({"topic": "battlestar galactica"})
rprint(results)
# 6. --------------------------------------------------
# Yes, that's a clever joke! It plays on the idea of Cylons from the "Battlestar Galactica" series, who are known for being artificial beings, while also using the pun on "human connection" to highlight the theme of 
# relationships. The blend of sci-fi and relationship humor makes it quite amusing!