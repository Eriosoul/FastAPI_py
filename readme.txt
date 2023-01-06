#http://127.0.0.1:8000/docs#/ para ver la documentacion
#http://127.0.0.1:8000/redoc segunda manera para ver la documentacion de nuestra api

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