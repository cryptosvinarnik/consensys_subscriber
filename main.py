import asyncio

from consensys import worker


async def main():
    q = asyncio.Queue()

    for email in open(input("File with emails >> ")).readlines():
        await q.put(email.strip())

    await asyncio.gather(
        *[worker(i, q) for i in range(1, 10)]
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

# create README.md for this project in the next commentary
# For install this script you need to install python3 and pip3
# Install the requirements:
# pip3 install -r requirements.txt
# Please fill the CAPMONSTER_API_KEY in the config.py file and write your emails in the emails.txt file
# Run the script:
# python3 main.py

