from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda x: {"foo": x}, name="first")


async def func(x):
    for _ in range(5):
        yield x


runnable2 = RunnableLambda(func, name="second")        

chain = runnable1 | runnable2


async def stream_events():
    async for event in chain.astream_events("bar", version="v2"):
        print(f"event={event['event']} | name={event['name']} | data={event['data']}")


import asyncio
asyncio.run(stream_events())
# event=on_chain_start | name=RunnableSequence | data={'input': 'bar'}
# event=on_chain_start | name=first | data={}
# event=on_chain_stream | name=first | data={'chunk': {'foo': 'bar'}}
# event=on_chain_start | name=second | data={}
# event=on_chain_end | name=first | data={'output': {'foo': 'bar'}, 'input': 'bar'}
# event=on_chain_stream | name=second | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=RunnableSequence | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=second | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=RunnableSequence | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=second | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=RunnableSequence | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=second | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=RunnableSequence | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=second | data={'chunk': {'foo': 'bar'}}
# event=on_chain_stream | name=RunnableSequence | data={'chunk': {'foo': 'bar'}}
# event=on_chain_end | name=second | data={'output': {'foo': 'bar'}, 'input': {'foo': 'bar'}}
# event=on_chain_end | name=RunnableSequence | data={'output': {'foo': 'bar'}}
