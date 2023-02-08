#Se importa el modulo FastAPi de la libreria fastapi
from fastapi import FastAPI

#Se crea una instancia de la clase FastAPI
app = FastAPI()

#Se crea un path operation decorator usando la funcion get
#En el home de la aplicacion se ejecutara nuestra funcion

@app.get("/")
def home():
    return {"message": "Hello World"}