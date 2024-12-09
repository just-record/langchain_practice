from dotenv import load_dotenv
load_dotenv()

# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

chain = (
    PromptTemplate.from_template(
        """Given the user question below, classify it as either being about `LangChain`, `Anthropic`, or `Other`.

Do not respond with more than one word.

<question>
{question}
</question>

Classification:"""
    )
    # | ChatAnthropic(model_name="claude-3-haiku-20240307")
    | ChatOpenAI(model_name="gpt-3.5-turbo")
    | StrOutputParser()
)

results = chain.invoke({"question": "how do I call Anthropic?"})
print(results)