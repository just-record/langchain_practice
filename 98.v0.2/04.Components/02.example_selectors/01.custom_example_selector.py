###The base interface

# class BaseExampleSelector(ABC):
#     """Interface for selecting examples to include in prompts."""

#     @abstractmethod
#     def select_examples(self, input_variables: Dict[str, str]) -> List[dict]:
#         """Select which examples to use based on the inputs."""
        
#     @abstractmethod
#     def add_example(self, example: Dict[str, str]) -> Any:
#         """Add new example to store."""


### Custom Example Selector

examples = [
    {"input": "hi", "output": "ciao"},
    {"input": "bye", "output": "arrivederci"},
    {"input": "soccer", "output": "calcio"},
]

## to pick based on the length of the word
from langchain_core.example_selectors.base import BaseExampleSelector


# 길이차이가 가장 작은 example을 선택
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
print(example_selector.select_examples({"input": "okay"}))
# [{'input': 'bye', 'output': 'arrivederci'}]

# add example
print('-'*30)
example_selector.add_example({"input": "hand", "output": "mano"})
print(example_selector.select_examples({"input": "okay"}))
# [{'input': 'hand', 'output': 'mano'}]


### Use in a Prompt
print('-'*30)
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
# Translate the following words from English to Italian:

# Input: hand -> Output: mano

# Input: word -> Output: