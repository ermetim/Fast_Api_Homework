from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI()

"""uvicorn main:app --reload
(запуск веб-сервера с указанием начального скрипта main.py и объекта
FastAPI который создали инструкцией app = FastAPI())
Обращение http://127.0.0.1:8000
"""

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return {'message': "service works"}


@app.post("/post")
def post() -> Timestamp:
    new_time = time.time()
    new_time_id = len(post_db)
    new_row = Timestamp(id = new_time_id, timestamp= int(round(new_time)))
    post_db.append(new_row)
    return new_row


@app.get("/dog")
def dog(kind: str):
    keys = []
    for key, val in dogs_db.items():
        if val.kind == kind:
            keys.append(key)
        lst = list(map(dogs_db.get, keys))
    if len(lst) == 0:
        raise HTTPException(status_code=409, detail='The specified KIND of dog is not exists.')
    return lst


@app.post("/dog") # Добавление
def dog(name: str,
        pk: int,
        kind: str):
    dog = Dog(name = name, pk = pk, kind = DogType(kind))
    for key, val in dogs_db.items():
        if val.pk == pk:
           raise HTTPException(status_code=409, detail='The specified PK already exists.')
    dogs_db[pk] = dog
    return dog

@app.post("/dog") # Добавление
def create_dog(name: str,
               pk: int,
               kind: str):
    dog = Dog(name = name, pk = pk, kind = DogType(kind))
    for key, val in dogs_db.items():
        if val.pk == pk:
           raise HTTPException(status_code=409, detail='The specified PK already exists.')
    dogs_db[pk] = dog
    return dog

# @app.post('/dog', response_model=Dog, summary='Create Dog')
# def create_dog(dog: Dog):
#     existing_pk = ...
#     if existing_pk:
#         raise HTTPException(status_code=409,
#                             detail='The specified PK already exists.')
#
#     ...
#
#     return Dog(...)
@app.get("/dog/{pk}")
def dog(pk: int) -> Dog:
    for key, val in dogs_db.items():
        if val.pk == pk:
            return dogs_db[key]
    raise HTTPException(status_code=409, detail='The specified PK is not exists.')

@app.patch("/dog/{pk}")
def dog(name: str,
        pk: int,
        kind: str) -> Dog:
    dog = Dog(name = name, pk = pk, kind = DogType(kind))
    for key, val in dogs_db.items():
        if val.pk == pk:
            dogs_db[key] = dog
            return dog
    raise HTTPException(status_code=409, detail='The specified PK is not exists.')













