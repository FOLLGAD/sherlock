import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from sherlock.sherlock import ask_sherlock
import uvicorn

class Item(BaseModel):
    input: str
    user_id: str
    user_name: str

app = FastAPI()

@app.post("/sherlock")
async def read_main(item: Item):
    task = asyncio.create_task(ask_sherlock(item.input, item.user_id, item.user_name))
    await asyncio.sleep(0)
    return await task

async def start():
    print("Starting HTTP handler...")
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()