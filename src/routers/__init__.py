from fastapi import APIRouter
from . import data, query # change here


router = APIRouter()
router.include_router(data.router)
router.include_router(query.router)

