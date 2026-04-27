import sys 
import os
import asyncio
import uvicorn
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.app import create_app

app = create_app()  # создаём приложение


async def run() -> None:
    config = uvicorn.Config(   # конифигурация сервера
        "main:app", 
        host="0.0.0.0",
        port=8000, 
        reload=True)
    # local-host - арендовали
    # сервер в Нидерландах,
    # у каждой штуки в сервере есть свой api-адрес, 127.0.0.1
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
