import asyncio

from loguru import logger

from consensys import worker


async def main():
    q = asyncio.Queue()

    with open("emails.txt") as f:
        accounts = f.read().splitlines()

    for account in accounts:
        if len(account.split("|")) == 2:
            q.put_nowait(account.split("|"))
        elif len(account.split("|")) == 1:
            q.put_nowait([account, None])
        else:
            logger.warning(f"Invalid account: {account}, skipping...")


    await asyncio.gather(
        *[worker(i, q) for i in range(1, 10)]
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
