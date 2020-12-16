async def arange(count: int):
    for i in range(count):
        yield(i)


async def alist(iterable):
    for i in iterable:
        yield(i)
