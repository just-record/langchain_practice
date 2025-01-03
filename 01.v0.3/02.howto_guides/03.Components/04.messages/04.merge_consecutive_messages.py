from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    merge_message_runs,
)

messages = [
    SystemMessage("you're a good assistant."),
    SystemMessage("you always respond with a joke."),
    HumanMessage([{"type": "text", "text": "i wonder why it's called langchain"}]),
    HumanMessage("and who is harrison chasing anyways"),
    AIMessage(
        'Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!'
    ),
    AIMessage("Why, he's probably chasing after the last cup of coffee in the office!"),
]

#################################################################################
### 1. merge_message_runs: 같은 타입의 메시지를 하나로 병합
print('1.', '-' * 50)
##################################################################################
merged = merge_message_runs(messages)
### merged ###
# rprint(merged)
# [
#     SystemMessage(content="you're a good assistant.\nyou always respond with a joke.", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content=[{'type': 'text', 'text': "i wonder why it's called langchain"}, 'and who is harrison chasing anyways'], additional_kwargs={}, response_metadata={}),
#     AIMessage(
#         content='Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!\nWhy, he\'s probably chasing after the last cup of coffee in the office!',
#         additional_kwargs={},
#         response_metadata={}
#     )
# ]

# print("\n\n".join([repr(x) for x in merged]))
for x in merged:
    rprint(repr(x))
# 1. --------------------------------------------------
# SystemMessage(content="you're a good assistant.\nyou always respond with a joke.", additional_kwargs={}, response_metadata={})
# HumanMessage(content=[{'type': 'text', 'text': "i wonder why it's called langchain"}, 'and who is harrison chasing anyways'], additional_kwargs={}, response_metadata={})
# AIMessage(content='Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!\nWhy, he\'s probably chasing after the last cup of coffee in the office!', additional_kwargs={}, response_metadata={})


#################################################################################
### 2. chaining
print('2.', '-' * 50)
##################################################################################
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0)
# Notice we don't pass in messages. This creates
# a RunnableLambda that takes messages as input
merger = merge_message_runs()
chain = merger | llm
rprint(chain.invoke(messages))
# 2. --------------------------------------------------
# AIMessage(
#     content=[],
#     additional_kwargs={},
#     response_metadata={
#         'id': 'msg_01QkyZcs12GDdZWJ1wuNEQWM',
#         'model': 'claude-3-sonnet-20240229',
#         'stop_reason': 'end_turn',
#         'stop_sequence': None,
#         'usage': {'input_tokens': 84, 'output_tokens': 3, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}
#     },
#     id='run-abc09206-b0d9-4e0a-b07d-f46bcceed586-0',
#     usage_metadata={'input_tokens': 84, 'output_tokens': 3, 'total_tokens': 87, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}}
# )


print(' ')
rprint(merger.invoke(messages))
# [
#     SystemMessage(content="you're a good assistant.\nyou always respond with a joke.", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content=[{'type': 'text', 'text': "i wonder why it's called langchain"}, 'and who is harrison chasing anyways'], additional_kwargs={}, response_metadata={}),
#     AIMessage(
#         content='Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!\nWhy, he\'s probably chasing after the last cup of coffee in the office!',
#         additional_kwargs={},
#         response_metadata={}
#     )
# ]


#################################################################################
### 3. prompt 뒤에 배치
print('3.', '-' * 50)
##################################################################################
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate(
    [
        ("system", "You're great a {skill}"),
        ("system", "You're also great at explaining things"),
        ("human", "{query}"),
    ]
)
chain = prompt | merger | llm
rprint(chain.invoke({"skill": "math", "query": "what's the definition of a convergent series"}))
# 3. --------------------------------------------------
# AIMessage(
#     content='A convergent series is an infinite series whose partial sums approach a finite value as more terms are added. In other words, the sequence of partial sums has a limit.\n\nMore formally, an infinite series Σ an 
# (where an are the terms of the series) is said to be convergent if the sequence of partial sums:\n\nS1 = a1\nS2 = a1 + a2  \nS3 = a1 + a2 + a3\n...\nSn = a1 + a2 + a3 + ... + an\n...\n\nconverges to some finite number S as n 
# goes to infinity. We write:\n\nlim n→∞ Sn = S\n\nThe finite number S is called the sum of the convergent infinite series.\n\nIf the sequence of partial sums does not approach any finite limit, the infinite series is said to be
# divergent.\n\nSome key properties:\n- A series converges if and only if the sequence of its partial sums is a Cauchy sequence.\n- Absolute/conditional convergence criteria help determine if a given series converges.\n- 
# Convergent series have many important applications in mathematics, physics, engineering etc.',
#     additional_kwargs={},
#     response_metadata={
#         'id': 'msg_018bNp2MefbAkGKyJyP6ymut',
#         'model': 'claude-3-sonnet-20240229',
#         'stop_reason': 'end_turn',
#         'stop_sequence': None,
#         'usage': {'input_tokens': 29, 'output_tokens': 268, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}
#     },
#     id='run-75f32609-002b-415e-be67-db54218cbf98-0',
#     usage_metadata={'input_tokens': 29, 'output_tokens': 268, 'total_tokens': 297, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}}
# )

print(' ')
chain = prompt | merger
rprint(chain.invoke({"skill": "math", "query": "what's the definition of a convergent series"}))
# [
#     SystemMessage(content="You're great a math\nYou're also great at explaining things", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content="what's the definition of a convergent series", additional_kwargs={}, response_metadata={})
# ]