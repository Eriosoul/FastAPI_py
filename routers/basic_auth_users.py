from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

#entidad usuario
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User):
    password: str


users_db = {
    "Eriosoul":{
        "username": "Eriosoul",
        "full_name": "Andrei Apostol",
        "email": "Eriosoul@erio.com",
        "disable": False,
        "password": "123456"
    },
    "Eriosoul2":{
        "username": "Eriosoul2",
        "full_name": "Andrei Apostol 2",
        "email": "Eriosoul2@erio.com",
        "disable": True,
        "password": "123"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

#criterio de dependencia
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autentificacion invalidas", 
            headers={"WWW-Authenticate": "Berarer"})

    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo", 
            headers={"WWW-Authenticate": "Berarer"})
    return user

#autentificacion
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)#comprobar si el usuario existe
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    return{"acces_token": user.username, "token_type": "Bearer"}

#ya autentificados
@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user