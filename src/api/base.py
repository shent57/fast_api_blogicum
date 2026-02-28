from fastapi import APIRouter

router = APIRouter(profile="/base")


@router.get("/hello_world")

async def get_hello_world():
    return Response(content="Hello, world", status_code=status.HTTP_200_OK)

@router.post("test_json")
async def test_json()