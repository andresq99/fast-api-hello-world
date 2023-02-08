#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#Se importa el modulo FastAPi de la libreria fastapi
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path

#Se crea una instancia de la clase FastAPI
app = FastAPI()

# Models

class Haircolor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name : str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = "Miguel"
        )
    last_name : str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = "Estrada"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example="25"
    )
    hair_color: Optional[Haircolor] = Field(default=None, example="black") # Valores opcionales
    is_married: Optional[bool] = Field(default=None, example=False) # Valores opcionales

    #class Config:
    #    schema_extra = {
    #        "example": {
    #            "first_name": "Facundo",
    #            "last_name": "Garcia Mantoni",
    #            "age": 21,
    #            "hair_color": "blonde",
    #            "is_married": False
    #        }
    #    }

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
#Query parameters
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title = "Perso Name",
        description= "This is the person name. It´s between 1 and 50 characters"
    ),
    age: str = Query(
        ..., 
        title="Person Age",
        description="This is the person age. Its required"
    )
):
    return {name : age}

# Validaciones: Path parameters

@app.get("/person/detail/{person_id}")
#Path parameter
def show_person(
    person_id: int = Path(..., 
                          gt=0,
                          title="Person Id",
                          description="Showing person id. Its required")
):
    return {person_id: "It exists"}

# Validaciones: Request Body
# Actualizar
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title ="Person ID",
        description = "This is the person ID",
        gt=0
    ),
    # Path operation (Que nos envio 2 request body)
    person: Person = Body(...),
    #location: Location = Body(...)
):
    #results = person.dict()
    #results.update(location.dict()) #Unir diccionarios
    #return results
    return person
