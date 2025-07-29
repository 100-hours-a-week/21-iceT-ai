from fastapi import APIRouter

from src.routers.v1.solution_router import router as solution_router_v1
from src.routers.v2.solution_router_v2 import router as solution_router_v2
from src.routers.v2.chatbot_router_v2 import router as chatbot_router_v2

router = APIRouter()

# v1 엔드포인트 등록
router.include_router(
    solution_router_v1,
    prefix="/api/ai/v1",
    tags=["해설지 생성 기능 v1"]
)

# v2 엔드포인트 등록
router.include_router(
    solution_router_v2,
    prefix="/api/ai/v2",
    tags=["해설지 생성 기능 v2"]
)
router.include_router(
    chatbot_router_v2,
    prefix="/api/ai/v2",
    tags=["챗봇 통합 기능 v2"]
)