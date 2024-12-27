from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini").bind(logprobs=True)

msg = llm.invoke(("human", "how are you today"))

#################################################################################
### 1. OpenAI API에서 로그 확률을 반환받으려면 logprobs=True 매개변수를 설정
### 해당 토큰이 등장할 로그 확률값 (음수가 작을수록 더 확실한 예측)
print('1.', '-' * 50)
##################################################################################
rprint(msg.response_metadata["logprobs"]["content"][:5])
# 1. --------------------------------------------------
# [
#     {'token': "I'm", 'bytes': [73, 39, 109], 'logprob': -0.062005553, 'top_logprobs': []},
#     {'token': ' just', 'bytes': [32, 106, 117, 115, 116], 'logprob': -0.031476747, 'top_logprobs': []},
#     {'token': ' a', 'bytes': [32, 97], 'logprob': -4.0961266e-05, 'top_logprobs': []},
#     {'token': ' computer', 'bytes': [32, 99, 111, 109, 112, 117, 116, 101, 114], 'logprob': -0.390251, 'top_logprobs': []},
#     {'token': ' program', 'bytes': [32, 112, 114, 111, 103, 114, 97, 109], 'logprob': -4.167649e-05, 'top_logprobs': []}
# ]


#################################################################################
### 2. 스트림에서 로그 확률 조회
print('2.', '-' * 50)
##################################################################################
ct = 0
full = None
for chunk in llm.stream(("human", "how are you today")):
    if ct < 5:
        full = chunk if full is None else full + chunk
        if "logprobs" in full.response_metadata:
            print(full.response_metadata["logprobs"]["content"])
    else:
        break
    ct += 1
# 2. --------------------------------------------------
# []
# [{'token': "I'm", 'bytes': [73, 39, 109], 'logprob': -0.04863608, 'top_logprobs': []}]
# [{'token': "I'm", 'bytes': [73, 39, 109], 'logprob': -0.04863608, 'top_logprobs': []}, {'token': ' just', 'bytes': [32, 106, 117, 115, 116], 'logprob': -0.031698626, 'top_logprobs': []}]
# [{'token': "I'm", 'bytes': [73, 39, 109], 'logprob': -0.04863608, 'top_logprobs': []}, {'token': ' just', 'bytes': [32, 106, 117, 115, 116], 'logprob': -0.031698626, 'top_logprobs': []}, {'token': ' a', 'bytes': [32, 97], 'logprob': -8.1490514e-05, 'top_logprobs': []}]
# [{'token': "I'm", 'bytes': [73, 39, 109], 'logprob': -0.04863608, 'top_logprobs': []}, {'token': ' just', 'bytes': [32, 106, 117, 115, 116], 'logprob': -0.031698626, 'top_logprobs': []}, {'token': ' a', 'bytes': [32, 97], 'logprob': -8.1490514e-05, 'top_logprobs': []}, {'token': ' computer', 'bytes': [32, 99, 111, 109, 112, 117, 116, 101, 114], 'logprob': -0.3920915, 'top_logprobs': []}]    