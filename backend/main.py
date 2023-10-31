from fastapi import FastAPI
from sqladmin import Admin, ModelView

from api import router
from api.auth.login import login_router
import uvicorn

from db.connect_db import engine
from db.models import User

app = FastAPI()
app.include_router(login_router)
app.include_router(router)

admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.user_id, User.name]


admin.add_view(UserAdmin)

if __name__ == "__main__":
    uvicorn.run(app=app, host='localhost', port=8000)
