from fastapi import APIRouter, UploadFile, File, Depends
from starlette.responses import JSONResponse
from database.db import get_db
from database.crud import *
from logger import logger

router_medias = APIRouter(prefix="/medias", tags=["Medias"])


@router_medias.post("/", response_class=JSONResponse)
async def load_file(
    file: UploadFile = File(...), db_session: AsyncSession = Depends(get_db)
):
    try:
        if file.size > 5242880:  # 5 Mb
            raise MaxSizeFile

        tdal = TweetDAL(db_session)
        file_id, file_ext = await tdal.add_file_to_db(file)
        await tdal.save_file(file, file_id, file_ext)
        return JSONResponse(content={"result": True, "media_id": file_id})

    except ApiKeyDontFind as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except FileDontSave as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except MaxSizeFile as e:
        error_text = e.text
        error_type = e.type
        logger.warning(error_type)

    except Exception:
        error_text = "Something wrong!"
        error_type = "Exception"
        logger.error(error_type)

    return JSONResponse(
        content={
            "result": False,
            "error_type": error_type,
            "error_message": error_text,
        }
    )
