# 입력값과 가장 유사한 예시를 선택하는 동시에 다양성을 최적화하는 방식으로 예시를 선택합니다. 이는 입력값과 코사인 유사도가 가장 높은 임베딩을 가진 예시들을 찾고, 이미 선택된 예시들과의 근접성에 대해 페널티를 부여하면서 반복적으로 추가하는 방식으로 작동합니다.

from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import (
    MaxMarginalRelevanceExampleSelector,
    SemanticSimilarityExampleSelector,
)
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

example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    # The list of examples available to select from.
    examples,
    # The embedding class used to produce embeddings which are used to measure semantic similarity.
    OpenAIEmbeddings(),
    # The VectorStore class that is used to store the embeddings and do a similarity search over.
    FAISS,
    # The number of examples to produce.
    k=2,
)
mmr_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Input: {adjective}\nOutput:",
    input_variables=["adjective"],
)


#################################################################################
### 1. # Input is a feeling, so should select the happy/sad example as the first one
print('1.', '-' * 50)
##################################################################################
print(mmr_prompt.format(adjective="worried"))
# 1. --------------------------------------------------
# Give the antonym of every input

# Input: happy
# Output: sad

# Input: windy
# Output: calm

# Input: worried
# Output:


#################################################################################
### 2. # Let's compare this to what we would just get if we went solely off of similarity,
###    # by using SemanticSimilarityExampleSelector instead of MaxMarginalRelevanceExampleSelector.
print('2.', '-' * 50)
##################################################################################
example_selector = SemanticSimilarityExampleSelector.from_examples(
    # The list of examples available to select from.
    examples,
    # The embedding class used to produce embeddings which are used to measure semantic similarity.
    OpenAIEmbeddings(),
    # The VectorStore class that is used to store the embeddings and do a similarity search over.
    FAISS,
    # The number of examples to produce.
    k=2,
)
similar_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Input: {adjective}\nOutput:",
    input_variables=["adjective"],
)
print(similar_prompt.format(adjective="worried"))
# 2. --------------------------------------------------
# Give the antonym of every input

# Input: happy
# Output: sad

# Input: sunny
# Output: gloomy

# Input: worried
# Output: