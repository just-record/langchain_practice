from dotenv import load_dotenv
load_dotenv()

from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import OpenAIEmbeddings

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}",
)

# Examples of a pretend task of creating antonyms.
examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"},
]

example_selector = SemanticSimilarityExampleSelector.from_examples(
    # The list of examples available to select from.
    examples,
    # The embedding class used to produce embeddings which are used to measure semantic similarity.
    OpenAIEmbeddings(),
    # The VectorStore class that is used to store the embeddings and do a similarity search over.
    Chroma,
    # The number of examples to produce.
    k=1,
)
similar_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Input: {adjective}\nOutput:",
    input_variables=["adjective"],
)


### 1. Input is a feeling, so should select the happy/sad example
print(similar_prompt.format(adjective="worried"))
# Give the antonym of every input

# Input: happy
# Output: sad

# Input: worried
# Output:


### 2. Input is a measurement, so should select the tall/short example
print('-'*30)
print(similar_prompt.format(adjective="large"))
# Give the antonym of every input

# Input: tall
# Output: short

# Input: large
# Output:


### 3. You can add new examples to the SemanticSimilarityExampleSelector as well
print('-'*30)
similar_prompt.example_selector.add_example(
    {"input": "enthusiastic", "output": "apathetic"}
)
print(similar_prompt.format(adjective="passionate"))
# Give the antonym of every input

# Input: enthusiastic
# Output: apathetic

# Input: passionate
# Output: