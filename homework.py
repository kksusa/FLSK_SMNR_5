from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


users = []


@app.get("/", response_model=list[User])
async def read_users():
    return users


@app.post("/user/", response_model=User)
async def create_user(item: User):
    id = len(users) + 1
    user = User
    user.id = id
    user.name = item.name
    user.email = item.email
    user.password = item.password
    users.append(user)
    return user


@app.get("/user/{id}", response_model=User)
async def get_user_by_id_root(id: int):
    for user in users:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/user/{id}", response_model=User)
async def put_user_by_id_root(id: int, new_user: User):
    for user in users:
        if user.id == id:
            user.name = new_user.name
            user.email = new_user.email
            user.password = new_user.password
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/user/{id}")
async def delete_user(id: int):
    for user in users:
        if user.id == id:
            users.remove(user)
            return users
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == '__main__':
    uvicorn.run(
        "homework:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
