import asyncio


async def foo():
    print('Async Basic')
    await asyncio.sleep(0.1)
    print('Async Sleep')
    return 'foo'


async def bar():
    x = await foo()
    print('bar:', x)

asyncio.run(bar())
