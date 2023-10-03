from fastapi import FastAPI
from api import router
from api.auth.login import login_router
import uvicorn

app = FastAPI()

app.include_router(login_router)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app=app, host='localhost', port=8000)
