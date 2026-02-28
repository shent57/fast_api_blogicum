from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from src.app import create_app

from api.base import router

from api.posts import router as posts_router

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




def create_app():
    app = FastAPI(root_path="/api/v1") 
# Нужно добавить обязательно: 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # с каких приложений можно запускать, * - все приложения
    allow_credentials=True,  # разрешаем аутентификацию, иначе авторизация недоступна
    allow_methods=["*"],   # можно вызывать только POST-методы
    allow_headers=["*"],   
    
    app.include_router(router, prefix="False")
)