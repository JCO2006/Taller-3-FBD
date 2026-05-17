from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


client = MongoClient(os.environ["MONGO_URI"])
# db = client["ISIS*******"]
db = client["ISIS2304B06202610"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    return list(db["comentarios"].find({"bar_id": bar_id}, {"_id": 0}))

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
    
    resultado = db.comentarios.insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    return list(db["eventos"].find({"bar_id": bar_id}, {"_id": 0}))


@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    
    datos['bar_id'] = bar_id
    datos['fechaInicio'] = datetime.now().isoformat()
    
    # Insertar el evento en la colección
    resultado = db.eventos.insert_one(datos)
    
    return {'mensaje': 'Evento guardado', 'id': str(resultado.inserted_id)}