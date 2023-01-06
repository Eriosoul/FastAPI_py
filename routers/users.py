from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

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

@router.get("/usersjson")
async def usersjson():
    return [{"name":"Andrei", "surname":"Apostol", "direcction":"Huerta abajo", "location":"Torrijos", "phone":666666666},
            {"name":"Andrei", "surname":"Apostol", "direcction":"Huerta abajo", "location":"Torrijos", "phone":666666666}]


@router.get("/users")
async def users():
    return users_list

#Path
@router.get("/user/{id}")
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
@router.get("/userquery/")
async def user(id: int):
    return search_user(id)

#inplementar un usuario nuevo 
@router.post("/user/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) ==User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

#actualizar datos
@router.put("/user/")
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_list): #buscamos en la lista de usuarios
        if saved_user.id == user.id: #si la informacion de los id son iguales lo encontramos
            users_list[index] = user #accedemos a indice de la lista
            found = True
    if not found:
        return{"Error":"No se ha encontrado el usuario"}
    else:
        return user

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, save_user in enumerate(users_list):
        if save_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return{"Error":"No se encontro el usuario"}
    else:
        return{"Eliminado":"El usuario ha sido eliminado"}

def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":" No se pudo encontrar el usuario"}