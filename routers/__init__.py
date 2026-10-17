from fastapi import APIRouter
from . import data, query


router = APIRouter()
router.include_router(data.router)
router.include_router(query.router)

