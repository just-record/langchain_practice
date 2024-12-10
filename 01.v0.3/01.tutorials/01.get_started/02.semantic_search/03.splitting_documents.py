from rich import print as rprint
from langchain_community.document_loaders import PyPDFLoader

file_path = "./nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

print(len(all_splits))
# 516

##################################################################################
### 1. 분할된 첫번 째 Document 보기
print('1.', '-' * 50)
##################################################################################
rprint(all_splits[0])
# Document(
#     metadata={'source': './nke-10k-2023.pdf', 'page': 0, 'start_index': 0},
#     page_content="Table of Contents\nUNITED STATES\nSECURITIES AND EXCHANGE COMMISSION\nWashington, D.C. 20549\nFORM 10-K\n(Mark One)\n☑  ANNUAL REPORT PURSUANT TO SECTION 13 
# OR 15(D) OF THE SECURITIES EXCHANGE ACT OF 1934\nFOR THE FISCAL YEAR ENDED MAY 31, 2023\nOR\n☐  TRANSITION REPORT PURSUANT TO SECTION 13 OR 15(D) OF THE SECURITIES EXCHANGE ACT
# OF 1934\nFOR THE TRANSITION PERIOD FROM                         TO                         .\nCommission File No. 1-10635\nNIKE, Inc.\n(Exact name of Registrant as specified in
# its charter)\nOregon 93-0584541\n(State or other jurisdiction of incorporation) (IRS Employer Identification No.)\nOne Bowerman Drive, Beaverton, Oregon 97005-6453\n(Address of
# principal executive offices and zip code)\n(503) 671-6453\n(Registrant's telephone number, including area code)\nSECURITIES REGISTERED PURSUANT TO SECTION 12(B) OF THE 
# ACT:\nClass B Common Stock NKE New York Stock Exchange\n(Title of each class) (Trading symbol) (Name of each exchange on which registered)"
# )

##################################################################################
### 2. 분할된 n번째(5번째) Document 보기
print('2.', '-' * 50)
##################################################################################
rprint(all_splits[4])
# 2. --------------------------------------------------
# Document(
#     metadata={'source': './nke-10k-2023.pdf', 'page': 0, 'start_index': 3276},
#     page_content="registrant's executive officers during the relevant recovery period pursuant to § 240.10D-1(b).\n¨ \n• whether the registrant is a shell company (as defined 
# in Rule 12b-2 of the Act). ☐ þ \nAs of November 30, 2022, the aggregate market values of the Registrant's Common Stock held by non-affiliates were:\nClass A $ 7,831,564,572 
# \nClass B 136,467,702,472 \n$ 144,299,267,044"
# )

### 첫번째 페이지의 마지막 문장 ###
### start_index가 3276 ###     
### 기본적으로 페이지 단위로 분할 된 다음 문장을 분할 하는 듯 ###


##################################################################################
### 3. 분할된 n번째(6번째) Document 보기
print('3.', '-' * 50)
##################################################################################
rprint(all_splits[5])
# 3. --------------------------------------------------
# Document(
#     metadata={'source': './nke-10k-2023.pdf', 'page': 1, 'start_index': 0},
#     page_content="Table of Contents\nAs of July 12, 2023, the number of shares of the Registrant's Common Stock outstanding were:\nClass A 304,897,252 \nClass B 1,225,074,356 
# \n1,529,971,608 \nDOCUMENTS INCORPORATED BY REFERENCE:\nParts of Registrant's Proxy Statement for the Annual Meeting of Shareholders to be held on September 12, 2023, are 
# incorporated by reference into Part III of this report."
# )
