from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint



from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # <-- Super slow! We can only make a request once every 10 seconds!!
    check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
    max_bucket_size=10,  # Controls the maximum burst size.
)


from langchain_openai import ChatOpenAI

model = ChatOpenAI(model_name="gpt-4o-mini", rate_limiter=rate_limiter)


#################################################################################
### 1. InMemoryRateLimiter: 단위 시간당 요청 수 제한
### 요청의 크기를 기준으로도 제한해야 하는 경우 X
print('1.', '-' * 50)
##################################################################################
import time

for _ in range(5):
    tic = time.time()
    model.invoke("hello")
    toc = time.time()
    print(toc - tic)
# 1. --------------------------------------------------
# 10.722046613693237
# 10.091930150985718
# 10.199786901473999
# 9.969878435134888
# 9.861935377120972   
