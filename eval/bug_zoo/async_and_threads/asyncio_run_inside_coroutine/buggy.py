"""Fetch two values concurrently."""

import asyncio


async def fetch(name):
    await asyncio.sleep(0)
    return {"name": name}


async def main():
    first = asyncio.run(fetch("a"))
    second = await fetch("b")
    print(first, second)


if __name__ == "__main__":
    asyncio.run(main())
