"""Load a user record asynchronously."""

import asyncio


async def load_user(user_id):
    await asyncio.sleep(0)
    return {"id": user_id, "name": "Ada"}


async def main():
    user = load_user(1)
    print(user["name"])


if __name__ == "__main__":
    asyncio.run(main())
