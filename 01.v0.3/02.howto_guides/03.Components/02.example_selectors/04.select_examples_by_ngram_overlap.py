# NGramOverlapExampleSelector는 n-gram 중첩 점수에 따라 입력과 가장 유사한 예시들을 선택하고 정렬합니다. n-gram 중첩 점수는 0.0에서 1.0 사이의 실수값입니다.
# 이 선택기는 임계값 점수를 설정할 수 있습니다. 임계값보다 작거나 같은 n-gram 중첩 점수를 가진 예시들은 제외됩니다. 기본적으로 임계값은 -1.0으로 설정되어 있어 어떤 예시도 제외하지 않고 단순히 재정렬만 합니다. 임계값을 0.0으로 설정하면 입력과 n-gram 중첩이 전혀 없는 예시들이 제외됩니다.

from langchain_community.example_selectors import NGramOverlapExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}",
)

# Examples of a fictional translation task.
examples = [
    {"input": "See Spot run.", "output": "Ver correr a Spot."},
    {"input": "My dog barks.", "output": "Mi perro ladra."},
    {"input": "Spot can run.", "output": "Spot puede correr."},
]

example_selector = NGramOverlapExampleSelector(
    # The examples it has available to choose from.
    examples=examples,
    # The PromptTemplate being used to format the examples.
    example_prompt=example_prompt,
    # The threshold, at which selector stops.
    # It is set to -1.0 by default.
    threshold=-1.0,
    # For negative threshold:
    # Selector sorts examples by ngram overlap score, and excludes none.
    # For threshold greater than 1.0:
    # Selector excludes all examples, and returns an empty list.
    # For threshold equal to 0.0:
    # Selector sorts examples by ngram overlap score,
    # and excludes those with no ngram overlap with input.
)
dynamic_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the Spanish translation of every input",
    suffix="Input: {sentence}\nOutput:",
    input_variables=["sentence"],
)


#################################################################################
### 1. # An example input with large ngram overlap with "Spot can run."
###    # and no overlap with "My dog barks."
print('1.', '-' * 50)
##################################################################################
print(dynamic_prompt.format(sentence="Spot can run fast."))
# 1. --------------------------------------------------
# Give the Spanish translation of every input

# Input: Spot can run.
# Output: Spot puede correr.

# Input: See Spot run.
# Output: Ver correr a Spot.

# Input: My dog barks.
# Output: Mi perro ladra.

# Input: Spot can run fast.
# Output:


#################################################################################
### 2. # You can add examples to NGramOverlapExampleSelector as well.
print('2.', '-' * 50)
##################################################################################
new_example = {"input": "Spot plays fetch.", "output": "Spot juega a buscar."}

example_selector.add_example(new_example)
print(dynamic_prompt.format(sentence="Spot can run fast."))
# 2. --------------------------------------------------
# Give the Spanish translation of every input

# Input: Spot can run.
# Output: Spot puede correr.

# Input: See Spot run.
# Output: Ver correr a Spot.

# Input: Spot plays fetch.
# Output: Spot juega a buscar.

# Input: My dog barks.
# Output: Mi perro ladra.

# Input: Spot can run fast.
# Output:


#################################################################################
### 3. # You can set a threshold at which examples are excluded.
###    # For example, setting threshold equal to 0.0
###    # excludes examples with no ngram overlaps with input.
###    # Since "My dog barks." has no ngram overlaps with "Spot can run fast."
###    # it is excluded.
print('3.', '-' * 50)
##################################################################################
example_selector.threshold = 0.0
print(dynamic_prompt.format(sentence="Spot can run fast."))
# 3. --------------------------------------------------
# Give the Spanish translation of every input

# Input: Spot can run.
# Output: Spot puede correr.

# Input: See Spot run.
# Output: Ver correr a Spot.

# Input: Spot plays fetch.
# Output: Spot juega a buscar.

# Input: Spot can run fast.
# Output:


#################################################################################
### 4. # Setting small nonzero threshold
print('4.', '-' * 50)
##################################################################################
example_selector.threshold = 0.09
print(dynamic_prompt.format(sentence="Spot can play fetch."))
# 4. --------------------------------------------------
# Give the Spanish translation of every input

# Input: Spot can run.
# Output: Spot puede correr.

# Input: Spot plays fetch.
# Output: Spot juega a buscar.

# Input: Spot can play fetch.
# Output:


#################################################################################
### 5. # Setting threshold greater than 1.0
print('5.', '-' * 50)
##################################################################################
example_selector.threshold = 1.0 + 1e-9
print(dynamic_prompt.format(sentence="Spot can play fetch."))
# 5. --------------------------------------------------
# Give the Spanish translation of every input

# Input: Spot can play fetch.
# Output: