# pip install pypdf

from rich import print as rprint
from langchain_community.document_loaders import PyPDFLoader

# file_path = "../example_data/nke-10k-2023.pdf"
file_path = "./nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

print(len(docs))
# 107

print(' ')
rprint(docs[0].page_content[:200])
# Table of Contents
# UNITED STATES
# SECURITIES AND EXCHANGE COMMISSION
# Washington, D.C. 20549
# FORM 10-K
# (Mark One)
# ☑  ANNUAL REPORT PURSUANT TO SECTION 13 OR 15(D) OF THE SECURITIES EXCHANGE ACT OF 1934
# F
print(' ')
rprint(docs[0].metadata)
# {'source': './nke-10k-2023.pdf', 'page': 0}
print(' ')
rprint(docs[0])
# Document(
#     metadata={'source': './nke-10k-2023.pdf', 'page': 0},
#     page_content="Table of Contents\nUNITED STATES\nSECURITIES AND EXCHANGE COMMISSION\nWashington, D.C. 20549\nFORM 10-K\n(Mark One)\n☑  ANNUAL REPORT PURSUANT TO SECTION 13 
# OR 15(D) OF THE SECURITIES EXCHANGE ACT OF 1934\nFOR THE FISCAL YEAR ENDED MAY 31, 2023\nOR\n☐  TRANSITION REPORT PURSUANT TO SECTION 13 OR 15(D) OF THE SECURITIES EXCHANGE ACT
# OF 1934\nFOR THE TRANSITION PERIOD FROM                         TO                         .\nCommission File No. 1-10635\nNIKE, Inc.\n(Exact name of Registrant as specified in
# its charter)\nOregon 93-0584541\n(State or other jurisdiction of incorporation) (IRS Employer Identification No.)\nOne Bowerman Drive, Beaverton, Oregon 97005-6453\n(Address of
# principal executive offices and zip code)\n(503) 671-6453\n(Registrant's telephone number, including area code)\nSECURITIES REGISTERED PURSUANT TO SECTION 12(B) OF THE 
# ACT:\nClass B Common Stock NKE New York Stock Exchange\n(Title of each class) (Trading symbol) (Name of each exchange on which registered)\nSECURITIES REGISTERED PURSUANT TO 
# SECTION 12(G) OF THE ACT:\nNONE\nIndicate by check mark: YES NO\n• if the registrant is a well-known seasoned issuer, as defined in Rule 405 of the Securities Act. þ ¨ \n• if 
# the registrant is not required to file reports pursuant to Section 13 or Section 15(d) of the Act. ¨ þ \n• whether the registrant (1) has filed all reports required to be filed
# by Section 13 or 15(d) of the Securities Exchange Act of 1934 during the preceding\n12 months (or for such shorter period that the registrant was required to file such 
# reports), and (2) has been subject to such filing requirements for the\npast 90 days.\nþ ¨ \n• whether the registrant has submitted electronically every Interactive Data File 
# required to be submitted pursuant to Rule 405 of Regulation S-T\n(§232.405 of this chapter) during the preceding 12 months (or for such shorter period that the registrant was 
# required to submit such files).\nþ ¨ \n• whether the registrant is a large accelerated filer, an accelerated filer, a non-accelerated filer, a smaller reporting company or an 
# emerging growth company. See the definitions of “large accelerated filer,”\n“accelerated filer,” “smaller reporting company,” and “emerging growth company” in Rule 12b-2 of the
# Exchange Act.\nLarge accelerated filer þ Accelerated filer ☐ Non-accelerated filer ☐ Smaller reporting company ☐ Emerging growth company ☐ \n• if an emerging growth company, if
# the registrant has elected not to use the extended transition period for complying with any new or revised financial\naccounting standards provided pursuant to Section 13(a) of
# the Exchange Act.\n¨ \n• whether the registrant has filed a report on and attestation to its management's assessment of the effectiveness of its internal control over 
# financial\nreporting under Section 404(b) of the Sarbanes-Oxley Act (15 U.S.C. 7262(b)) by the registered public accounting firm that prepared or issued its audit\nreport.\nþ 
# \n• if securities are registered pursuant to Section 12(b) of the Act, whether the financial statements of the registrant included in the filing reflect the\ncorrection of an 
# error to previously issued financial statements.\n¨ \n• whether any of those error corrections are restatements that required a recovery analysis of incentive-based 
# compensation received by any of the\nregistrant's executive officers during the relevant recovery period pursuant to § 240.10D-1(b).\n¨ \n• whether the registrant is a shell 
# company (as defined in Rule 12b-2 of the Act). ☐ þ \nAs of November 30, 2022, the aggregate market values of the Registrant's Common Stock held by non-affiliates were:\nClass A
# $ 7,831,564,572 \nClass B 136,467,702,472 \n$ 144,299,267,044 "
# )
