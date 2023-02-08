#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#Se importa el modulo FastAPi de la libreria fastapi
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query

#Se crea una instancia de la clase FastAPI
app = FastAPI()

# Models

class Person(BaseModel):
    first_name : str
    last_name : str
    age: int
    hair_color: Optional[str] = None # Valores opcionales
    is_married: Optional[bool] = None # Valores opcionales


#Se crea un path operation decorator usando la funcion get
#En el home de la aplicacion se ejecutara nuestra funcion

@app.get("/") #Path operation decorator: Permite que la operation function acceda a una path ejecutando la definicion de la funcion
def home(): # Path operation function
    return {"message": "Hello World"}

# Request and Responde Body

@app.post("/person/new") # Enviar datos desde el cliente al servidor
def create_person(person: Person = Body(...)):
    return person

#Validaciones query parameter

@app.get("/person/detail")
def show_person(name: Optional[str] = Query(None, min_length=1, max_length=50),age: str = Query(...)):
    return {name : age}
                


