from enum import Enum

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

"""
Запуск локально
uvicorn main:app --reload
(запуск веб-сервера с указанием начального скрипта main.py и объекта
FastAPI который создали инструкцией app = FastAPI())
Обращение http://127.0.0.1:8000

Запуск на рендере
# uvicorn main:app --host 0.0.0.0 --port 8000 # For render.com

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
def get_post() -> Timestamp:
    new_time = time.time()
    new_time_id = len(post_db)
    new_row = Timestamp(id = new_time_id, timestamp= int(round(new_time)))
    post_db.append(new_row)
    return new_row


@app.get("/dog", summary="Get Dogs")
def get_dogs(kind: DogType = None) -> List[Dog]:
    if kind is None:
        return list(dogs_db.values())
    keys = []
    for key, val in dogs_db.items():
        if val.kind == kind.lower():
            keys.append(key)
    lst = list(map(dogs_db.get, keys))
    if len(lst) == 0:
        raise HTTPException(status_code=409, detail='The specified KIND of dog does not exist.')
    return lst


@app.post("/dog", response_model=Dog, summary="Create Dog") # Добавление собаки в базу
def create_dog(dog: Dog) -> Dog:
    if dog.pk in dogs_db:
        raise HTTPException(status_code=409, detail='The specified PK already exists.')
    dogs_db[dog.pk] = dog
    return dog


@app.get("/dog/{pk}", response_model=Dog, summary="Get Dog by PK")
def get_dog_pk(pk: int) -> Dog:
    if pk not in dogs_db:
        raise HTTPException(status_code=409, detail='The specified PK does not exist.')
    return dogs_db[pk]

@app.patch("/dog/{pk}", response_model=Dog, summary='Update Dog')
def update_dog(pk: int, dog: Dog) -> Dog:
    if pk not in dogs_db:
        raise HTTPException(status_code=409, detail='The specified PK does not exist.')
    if pk != dog.pk:
        raise HTTPException(status_code=409, detail='The specified PK does not match.')
    dogs_db[pk] = dog
    return dog
