from langchain_core.prompts import PromptTemplate

example_prompt = PromptTemplate.from_template("Question: {question}\n{answer}")

### example_prompt 출력
print(example_prompt)
# input_variables=['answer', 'question'] template='Question: {question}\n{answer}'

### few-shot example set
examples = [
    {
        "question": "Who lived longer, Muhammad Ali or Alan Turing?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali
""",
    },
    {
        "question": "When was the founder of craigslist born?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the founder of craigslist?
Intermediate answer: Craigslist was founded by Craig Newmark.
Follow up: When was Craig Newmark born?
Intermediate answer: Craig Newmark was born on December 6, 1952.
So the final answer is: December 6, 1952
""",
    },
    {
        "question": "Who was the maternal grandfather of George Washington?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the mother of George Washington?
Intermediate answer: The mother of George Washington was Mary Ball Washington.
Follow up: Who was the father of Mary Ball Washington?
Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
So the final answer is: Joseph Ball
""",
    },
    {
        "question": "Are both the directors of Jaws and Casino Royale from the same country?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who is the director of Jaws?
Intermediate Answer: The director of Jaws is Steven Spielberg.
Follow up: Where is Steven Spielberg from?
Intermediate Answer: The United States.
Follow up: Who is the director of Casino Royale?
Intermediate Answer: The director of Casino Royale is Martin Campbell.
Follow up: Where is Martin Campbell from?
Intermediate Answer: New Zealand.
So the final answer is: No
""",
    },
]

### example set중 하나를 example_prompt에 적용
print('-'*30)
results = example_prompt.invoke(examples[0])
print(results)
# text='Question: Who lived longer, Muhammad Ali or Alan Turing?\n\nAre follow up questions needed here: Yes.\nFollow up: How old was Muhammad Ali when he died?\nIntermediate answer: Muhammad Ali was 74 years old when he died.\nFollow up: How old was Alan Turing when he died?\nIntermediate answer: Alan Turing was 41 years old when he died.\nSo the final answer is: Muhammad Ali\n'


### FewShotPromptTemplate 사용
print('-'*30)

from langchain_core.prompts import FewShotPromptTemplate

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"],
)

print(
    prompt.invoke({"input": "Who was the father of Mary Ball Washington?"}).to_string()
)
# Question: Who lived longer, Muhammad Ali or Alan Turing?

# Are follow up questions needed here: Yes.
# Follow up: How old was Muhammad Ali when he died?
# Intermediate answer: Muhammad Ali was 74 years old when he died.
# Follow up: How old was Alan Turing when he died?
# Intermediate answer: Alan Turing was 41 years old when he died.
# So the final answer is: Muhammad Ali


# Question: When was the founder of craigslist born?

# Are follow up questions needed here: Yes.
# Follow up: Who was the founder of craigslist?
# Intermediate answer: Craigslist was founded by Craig Newmark.
# Follow up: When was Craig Newmark born?
# Intermediate answer: Craig Newmark was born on December 6, 1952.
# So the final answer is: December 6, 1952


# Question: Who was the maternal grandfather of George Washington?

# Are follow up questions needed here: Yes.
# Follow up: Who was the mother of George Washington?
# Intermediate answer: The mother of George Washington was Mary Ball Washington.
# Follow up: Who was the father of Mary Ball Washington?
# Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
# So the final answer is: Joseph Ball


# Question: Are both the directors of Jaws and Casino Royale from the same country?

# Are follow up questions needed here: Yes.
# Follow up: Who is the director of Jaws?
# Intermediate Answer: The director of Jaws is Steven Spielberg.
# Follow up: Where is Steven Spielberg from?
# Intermediate Answer: The United States.
# Follow up: Who is the director of Casino Royale?
# Intermediate Answer: The director of Casino Royale is Martin Campbell.
# Follow up: Where is Martin Campbell from?
# Intermediate Answer: New Zealand.
# So the final answer is: No


# Question: Who was the father of Mary Ball Washington?