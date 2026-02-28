import asyncio
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(root_path="/api/v1") 
# Нужно добавить обязательно: 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # с каких приложений можно запускать, * - все приложения
    allow_credentials=True,  # разрешаем аутентификацию, иначе авторизация недоступна
    allow_methods=["*"],   # можно вызывать только POST-методы
    allow_headers=["*"],   
)

# Как запустить fast-api приложение


async def run() -> None:
    config = uvicorn.Config("main:app", host="0.0.0.0", 
                            port=8000, reload=False) # local-host - арендовали
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
