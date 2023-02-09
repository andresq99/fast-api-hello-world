#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#Se importa el modulo FastAPi de la libreria fastapi
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import Form # Viene de un formulario
from fastapi import Header # Viene de un header
from fastapi import Cookie # Viene de una cookie
from fastapi import UploadFile # Viene de un archivo
from fastapi import File # Viene de un archivo
from fastapi import HTTPException # Manejo de excepciones
from fastapi import status # Acceder a los codigos de estado HTTP 

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

class PersonBase(BaseModel): # Herencia de Person y PersonOut
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

class PersonOut(PersonBase):
    pass

class Person(PersonBase):
    password: str = Field(..., min_length=8)
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

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="miguel2021")
    message: str = Field(default="Login successfully")

#Se crea un path operation decorator usando la funcion get
#En el home de la aplicacion se ejecutara nuestra funcion

@app.get(
        path="/",
        status_code=status.HTTP_200_OK
        ) #Path operation decorator: Permite que la operation function acceda a una path ejecutando la definicion de la funcion
def home(): # Path operation function
    return {"message": "Hello World"}
 
# Request and Responde Body
# Parth Operations

#Devolver solo los datos de PersonOut
#Endpoint para crear una persona
@app.post(
        path="/person/new",
        response_model=PersonOut,
        status_code=status.HTTP_201_CREATED
        ) # Enviar datos desde el cliente al servidor
def create_person(person: Person = Body(...)): # Request Body
    return person

#Validaciones query parameter
#Obteniendo un resultado
@app.get(
        path="/person/detail",
        status_code=status.HTTP_200_OK
        ) # Decorador
#Query parameters
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title = "Perso Name",
        description= "This is the person name. It´s between 1 and 50 characters",
        example="Rocio"
    ),
    age: str = Query(
        ..., 
        title="Person Age",
        description="This is the person age. Its required",
        example=25
    )
):
    return {name : age}

# Validaciones: Path parameters

persons = [1,2,3,4,5]

@app.get(
        path="/person/detail/{person_id}",
        status_code=status.HTTP_200_OK
        )
#Path parameter
def show_person(
    person_id: int = Path(..., 
                          gt=0,
                          example=123,
                          title="Person Id",
                          description="Showing person id. Its required")
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person does not exist"
        )
    return {"person_id": "It exists"}

# Validaciones: Request Body
# Actualizar
@app.put(
        "/person/{person_id}",
        status_code=status.HTTP_202_ACCEPTED
        )
def update_person(
    person_id: int = Path(
        ...,
        title ="Person ID",
        description = "This is the person ID",
        gt=0,
        example=123
    ),
    # Path operation (Que nos envio 2 request body)
    person: Person = Body(...),
    #location: Location = Body(...)
):
    #results = person.dict()
    #results.update(location.dict()) #Unir diccionarios
    #return results
    return person

#Path operation
#Formularios
#Del backend al fronetnd

#Logeando una cuenta
@app.post(
    path = "/login",
    response_model= LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Cookies and Headers Parameters

@app.post(
    path = "/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent
    
# Files

@app.post(
    path = "/post-image"
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024,ndigits=2)
    }
