#Se importa el modulo FastAPi de la libreria fastapi
from fastapi import FastAPI

#Se crea una instancia de la clase FastAPI
app = FastAPI()

#Se crea un path operation decorator usando la funcion get
#En el home de la aplicacion se ejecutara nuestra funcion

@app.get("/") #Path operation decorator: Permite que la operation function acceda a una path ejecutando la definicion de la funcion
def home(): # Path operation function
    return {"message": "Hello World"}