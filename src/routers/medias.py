from fastapi import APIRouter, UploadFile, File, Depends
from starlette.responses import JSONResponse
from database.db import get_db
from database.crud import *

router_medias = APIRouter(prefix="/medias", tags=["Medias"])


@router_medias.post("/", response_class=JSONResponse)
async def load_file(file: UploadFile = File(...), db_session: AsyncSession = Depends(get_db)):
    tdal = TweetDAL(db_session)
    file_id, file_ext = await tdal.add_file_to_db(file)
    await tdal.save_file(file, file_id, file_ext)
    return JSONResponse(content={"result": True, "media_id": file_id})
