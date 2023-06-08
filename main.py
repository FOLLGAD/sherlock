#!/usr/bin/env python3

import asyncio

# import env variables first
from dotenv import load_dotenv
load_dotenv()

from handlers.telegram import start as start_telegram
from handlers.http import start as start_http

async def main():
    await asyncio.gather(start_telegram(), start_http())

if __name__ == "__main__":
    asyncio.run(main())