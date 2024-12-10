from rich import print as rprint
from langchain_core.documents import Document

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

rprint(documents)
# [
#     Document(metadata={'source': 'mammal-pets-doc'}, page_content='Dogs are great companions, known for their loyalty and friendliness.'),
#     Document(metadata={'source': 'mammal-pets-doc'}, page_content='Cats are independent pets that often enjoy their own space.')
# ]

print(' ')

print(documents[0].page_content)
print(documents[0].metadata)
print(documents[0].metadata['source'])
# Dogs are great companions, known for their loyalty and friendliness.
# {'source': 'mammal-pets-doc'}
# mammal-pets-doc