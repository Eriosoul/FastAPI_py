from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId


router = APIRouter()

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"menssage": "No content"}})

users_list = []

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

#@router.get("/users")
#async def users():
#    return users_list

@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    #else:
    #acceder a nuestra base de datos
    user_dict = dict(user)# lo transformamos en un dicionario
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id #el contenido user se debe transformar en un json
    
    #comprobacion de ID en la base de datos
    #cuando le decimos que pase le indicamos el id pero cual? el que se introdujo
    new_user =user_schema(db_client.users.find_one({"_id": id}))
    return User(**new_user)

@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    #para no actualizar el campo id
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return{"Error":"No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return{"Error":"No se encontro el usuario"}
    else:
        return{"Eliminado":"El usuario ha sido eliminado"}

def search_user(field: str, key):
    # le pasamos el criterio de busqueda y la clave de busqueda
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error":" No se pudo encontrar el usuario"}
