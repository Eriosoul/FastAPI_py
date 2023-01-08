from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 1
SECRET = "85709c93f5e544c2973d5e4cd266c42840c01a4eddfd06c3ca4fe7b64b67225275003d0f4d0507f85fef7938d3d3e584dbf521170c4dfaa4c842c9f5644091884aae0365c93c40969a20a77b3f677e3f"

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$k5SQjMxRrQaFekee1P3KN.XmwAw25TbKVqgkzzq354Wz9oO1WQT/W"
    },
    "Eriosoul2":{
        "username": "Eriosoul2",
        "full_name": "Andrei Apostol 2",
        "email": "Eriosoul2@erio.com",
        "disable": True,
        "password": "$2a$12$h.o75ranSWYgloVGpdy6gebaLRhYYX4mHmkuA3FKMDjN0QDklPfwK"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exeption = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autentificacion invalidas", 
            headers={"WWW-Authenticate": "Berarer"})
    try:
        username = jwt.decode(token, SECRET,
                    algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exeption
        
    except JWTError:
        raise exeption

    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo", 
            headers={"WWW-Authenticate": "Berarer"})
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)#comprobar si el usuario existe
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)    

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    acces_token = {"sub":user.username, 
                   "exp": datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)}

    return{"acces_token": jwt.encode(acces_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.post("/users/me")
async def me(user: User = Depends(current_user)):
    return user