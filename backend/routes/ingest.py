from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

import backend.models.api as api_models, backend.models.ingest as ingest_models
from backend.data.storage import storage
from backend.websocket import socket_manager

ingest_router = APIRouter()


# check status of ingest (get)
@ingest_router.get("/status")
async def status():
    return api_models.Success()


# push uid to storage (post)
@ingest_router.post("/push-uid")
async def push_uid(body: ingest_models.UIDModel):
    uid = storage.push_uid(body.uid)
    if uid is not None:
        await socket_manager.broadcast(uid)
        return JSONResponse(content={"status": "success"}, status_code=200)
    else:
        return JSONResponse(content={"status": "error"}, status_code=500)
