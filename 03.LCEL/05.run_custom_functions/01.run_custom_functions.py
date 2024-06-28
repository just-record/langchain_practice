from dotenv import load_dotenv
load_dotenv()

from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


def length_function(text):
    return len(text)


def _multiple_length_function(text1, text2):
    return len(text1) * len(text2)


def multiple_length_function(_dict):
    return _multiple_length_function(_dict["text1"], _dict["text2"])


model = ChatOpenAI()

prompt = ChatPromptTemplate.from_template("what is {a} + {b}")

chain1 = prompt | model

chain = (
    {
        "a": itemgetter("foo") | RunnableLambda(length_function),
        "b": {"text1": itemgetter("foo"), "text2": itemgetter("bar")}
        | RunnableLambda(multiple_length_function),
    }
    | prompt
    | model
    | StrOutputParser()
)

results = chain.invoke({"foo": "bar", "bar": "gah"})
print(results)