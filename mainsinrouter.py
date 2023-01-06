from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():#async se encarga de ir actualizando la info de la pagina web
    return "message Hello World"


@app.get("/url")
async def url():
    return {"message":"www.youtube.com/eriosoul"} #devolvemos un json



#http://127.0.0.1:8000/docs#/ para ver la documentacion
#http://127.0.0.1:8000/redoc segunda manera para ver la documentacion de nuestra api
