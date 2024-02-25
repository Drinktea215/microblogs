from routers.users import router_users
from routers.tweets import router_tweets
from routers.medias import router_medias
from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI(title="Microblogs")

api = APIRouter(prefix="/api", tags=["Api"])

api.include_router(router_users)
api.include_router(router_tweets)
api.include_router(router_medias)

app.include_router(api)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
