from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/source", StaticFiles(directory="source"), name="source")