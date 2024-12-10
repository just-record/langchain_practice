# Tutorials - Get Started - Build a semantic search engine

<https://python.langchain.com/docs/tutorials/retrievers/>

## Documents and Document Loaders

- 01.documents.py: Document 객체
- 02.loading_documents.py: PDF 파일 로드
  - <https://github.com/langchain-ai/langchain/tree/master/docs/docs/example_data>
- 03.splitting_documents.py: 문서 분할  

## Embeddings

- 04.embeddings_openai.py: Embedding 하기 - OpenAI
- 05.embeddings_huggingface.py: Embedding 하기 - Hugging Face

## Vector Stores

- 06.vector_stores_in_memory.py: 메모리에 벡터 저장
- 07.vector_stores_chroma.py: Chroma에 벡터 저장
- 08.vector_stores_faiss.py: Faiss에 벡터 저장

✔️ FAISS는 공식 문서의 소스 코드가 오류 발생 - 시간을 두고 분석 할 필요 있음
`TypeError: FAISS.__init__() missing 3 required positional arguments: 'index', 'docstore', and 'index_to_docstore_id'`

## Retrievers

- 09.retrievers.py: Faiss로 검색



