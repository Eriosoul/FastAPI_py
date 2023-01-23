#http://127.0.0.1:8000/docs#/ para ver la documentacion
#http://127.0.0.1:8000/redoc segunda manera para ver la documentacion de nuestra api
Bases de datos MongoDB
FastAPI, passlib[bcrypt], python-jose[cryptography]
Thunder client para comprobacion de si finciona o no 

Iniciar el servidor: uvicorn main:app --reload

Mediante el framewor thunder client hemos ido viendo como va nuestras peticiones en servidor
POST: pedir datos
GET: leer los datos
PUT: modificar/actualizar los datos
DELETE: eliminar los datos

CRUD: CREATE READ UPDATE DELETE




API DE USUARIOS
Debemos crear un metodo para indicar la informacion que solicitara al usario
Importamos lo siguente para indicar un modelo base: from pydantic import BaseModel 

Codigos de estados
200: todo ok
201: Created
202: Acepted
204: No content
300: Redirect
304: Not Modificated
404: Not Found

raise: propaga la expecion de los errores
detail: nos indica la informacion que escribimos a la hora de error
response_model= nos indicara lo que responde, en caso de que funcione bien o de que funcione mal


Para poder acceder a diferentes archivos procedemos a crear una carpeta routerst, movemos la informacion a esa carpeta

#routers
app.include_router(products.router)
asi procedemos a anidar la infromacion de diversos ficheros productos usuarios etc..

Para no estar indicando siempre la ruta en 
@router.get("/products")
Podemos ralizar el siguente metodo
router = APIRouter(prefix="/products")
y el @router.get("/products") quedaria @router.get("/")


Para JWT se ha procedio a instalar 
pip install "passlib[bcrypt]"
pip install "python-jose[cryptography]"

A la hora de iniciar el mongodDB
"C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath="c:\data\db"
--dbpath="c:\data\db" 

Asi podremos arrancar la instancia

pip install pymongo 