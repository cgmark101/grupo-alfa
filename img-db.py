import os, shutil, re
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from tinydb import TinyDB, Query
from tinydb.table import Document
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = "static/images/person"

db = TinyDB('db.json')

class Person(BaseModel):
    img: str
    nombre: str
    cargo: str

app = FastAPI()

path = os.path.join(BASE_DIR, STATIC_DIR)

@app.get('/all')
async def get_data():
    search = db.all()
    return search

@app.get('/image')
async def get_data(nombre:str):
    search = db.search(Query().nombre == nombre.lower())
    return search

@app.post("/image")
async def post_data(nombre:str, cargo:str, image:UploadFile = File(...)):
    search = db.search(Query().nombre == nombre.lower())
    longitud=len(db)
    url_search = db.search(Query().url == nombre.lower())
    archivo = f'person_{longitud + 1}.png'
    if longitud != 0:
        archivo = f'person_{longitud + 1}.webp'
        print(longitud)
        print(search)
        payload = {
            'url': f'{STATIC_DIR}/{archivo}',
            'nombre': nombre.lower(),
            'cargo': cargo.lower()
        }
        img = os.path.join(BASE_DIR, "static/images/person")
        list = os.listdir(img)
        if f'{archivo}.webp' in list:
            return 'archivo existe'
        elif db.search(Query().nombre.matches(nombre, flags=re.IGNORECASE)): 
            return 'trabajador existe'
        else:
            with open(f'{path}/{archivo}', "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            db.insert(payload)
            return payload
    else:
        archivo = f'person_1.png'
        payload = {
            'url': f'{STATIC_DIR}/{archivo}',
            'nombre': nombre.lower(),
            'cargo': cargo.lower(),
        }
        with open(f'{path}/{archivo}', "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            db.insert(payload)
            return payload

@app.put('/image')
async def edit_data(busqueda:str, cargo:str, image:UploadFile = File(...), nombre:Optional[str]=None):
    search = db.search(Query().nombre == busqueda.lower())
    if db.search(Query().nombre.matches(busqueda, flags=re.IGNORECASE)): 
        if nombre == None:
            payload = {
                'url': search[0]['url'],
                'nombre': busqueda.lower(),
                'cargo': cargo.lower()
            }
            with open(search[0]['url'], "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
                update = db.update(payload)
                return update
        else:
            payload = {
                'url': search[0]['url'],
                'nombre': nombre.lower(),
                'cargo': cargo.lower()
            }
            with open(search[0]['url'], "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
                update = db.update(payload)
                return update

    else:
        return 'trabajor no existe'

@app.delete('/image')
async def delete_data(nombre:str):
    key = db.get(Query().nombre == nombre.lower())
    if key == None:
        return 'trabajador no existe'
    else:
        db.remove(doc_ids=[key.doc_id])
        os.remove(key['url'])
        db.insert(Document({}, doc_id=key.doc_id))
        return f"trabajador {key['nombre']} removido"