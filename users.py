from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Iniciar la app: uvicorn users:app --reload

# Creamos la entidad del usuario
class User(BaseModel):# Nos da la capacidad de crear una entidad
    id: int
    name: str
    surname: str
    direcction: str
    location: str
    phone: int

users_list = [User(id=1,name="Andrei", surname="Apostol", direcction="Huerta abajo", location="Torrijos",phone=666),   
              User(id=2,name="Diana", surname="Apostol",direcction="Huerta abajo", location="Torrijos", phone=446),
              User(id=3,name="Pepe", surname="Palote",direcction="Huerta abajo", location="Camarena", phone=556)]

@app.get("/usersjson")
async def usersjson():
    return [{"name":"Andrei", "surname":"Apostol", "direcction":"Huerta abajo", "location":"Torrijos", "phone":666666666},
            {"name":"Andrei", "surname":"Apostol", "direcction":"Huerta abajo", "location":"Torrijos", "phone":666666666}]


@app.get("/users")
async def users():
    return users_list

#Path
@app.get("/user/{id}")
async def user(id: int):
    #usamos el metodo filter para filrtar el id de la lista de usuarios
    #se lo pasamos a una variable y listamos dicha variable
    users = filter(lambda user: user.id == id, users_list)
    #para que no nos devuelva un listado debemos indicarle que debemos ir  ala primera posicion
    try:
        return list(users)[0]
    except:
        return {"error":" No se pudo encontrar el usuario"}
#Query
@app.get("/userquery/")
async def user(id: int):
    return search_user(id)

def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":" No se pudo encontrar el usuario"}
