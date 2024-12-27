from rich import print as rprint

examples = [
    {"input": "hi", "output": "ciao"},
    {"input": "bye", "output": "arrivederci"},
    {"input": "soccer", "output": "calcio"},
]


from langchain_core.example_selectors.base import BaseExampleSelector


#################################################################################
### 1. Custom Example Selector
print('1.', '-' * 50)
##################################################################################
class CustomExampleSelector(BaseExampleSelector):
    def __init__(self, examples):
        self.examples = examples

    def add_example(self, example):
        self.examples.append(example)

    def select_examples(self, input_variables):
        # This assumes knowledge that part of the input will be a 'text' key
        new_word = input_variables["input"]
        new_word_length = len(new_word)

        # Initialize variables to store the best match and its length difference
        best_match = None
        smallest_diff = float("inf")

        # Iterate through each example
        for example in self.examples:
            # Calculate the length difference with the first word of the example
            current_diff = abs(len(example["input"]) - new_word_length)

            # Update the best match if the current one is closer in length
            if current_diff < smallest_diff:
                smallest_diff = current_diff
                best_match = example

        return [best_match]
    
    
example_selector = CustomExampleSelector(examples)
rprint(example_selector.select_examples({"input": "okay"}))
# 1. --------------------------------------------------
# [{'input': 'bye', 'output': 'arrivederci'}]

#################################################################################
### 2. Custom Example Selector - add_example
print('2.', '-' * 50)
##################################################################################
example_selector.add_example({"input": "hand", "output": "mano"})
rprint(example_selector.select_examples({"input": "okay"}))
# 2. --------------------------------------------------
# [{'input': 'hand', 'output': 'mano'}]


#################################################################################
### 3. 프롬프트에서 사용하기
print('3.', '-' * 50)
##################################################################################
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate

example_prompt = PromptTemplate.from_template("Input: {input} -> Output: {output}")

prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    suffix="Input: {input} -> Output:",
    prefix="Translate the following words from English to Italian:",
    input_variables=["input"],
)

print(prompt.format(input="word"))
# 3. --------------------------------------------------
# Translate the following words from English to Italian:

# Input: hand -> Output: mano

# Input: word -> Output:
