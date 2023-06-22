from enum import Enum
from fastapi import FastAPI, Query
from pydantic import BaseModel

#https://fastapi.tiangolo.com/pt/tutorial/path-params-numeric-validations/

app = FastAPI()

class Sexo(str,Enum):
    Masculino = 'M'
    Feminino = 'F'
    Calango = '?'

class Pessoa(BaseModel):
    nome: str
    idade: int
    sexo: Sexo | None = None
    salario: float | None = None

fake_users_db = [
        {'name':"Alexandre",'idade':23,'sexo':"Masculino"},
        {'name':"Maria",'idade':25,'sexo':"Feminino"},
        {'name':"João",'idade':15,'sexo':"Calango"},
        {'name':"Marcos",'idade':29,'sexo':"Masculino"}
    ]

@app.put("/users/{user_id}")
def change_user(id_pessoa: int, pessoa: Pessoa):
    pessoa : dict =  {
        "id_pessoa": id_pessoa,
        **pessoa.dict()
    }
    return pessoa

@app.post("/users/")
def create_user(pessoa: Pessoa):
    return pessoa

@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(
    user_id: int, item_id: int, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item

@app.get("/itens_needy/{item_id}")
def read_item_needy(item_id: str, needy:str, opcional: str | None = None):
    item = {"item_id": item_id, "needy": needy,"opcional": opcional}
    return item

@app.get("/items/{item_id}")
def item(item_id : int,
        q : list[str] | None = Query(default=..., max_length=50, min_length=1, title='Query String',description='Query string description', alias='Q Query alias',deprecated=True),
        short : bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item

@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    return fake_users_db[skip : skip + limit]

@app.get("/models/{model_name}")
def model(model_name : Sexo):
    if model_name == Sexo.Masculino:
        return {"sexo": model_name, "message": "Vuser é homim"}
    
    if model_name.value == 'lenet':
        return {"sexo": model_name, "message": "Vuser é muier"}
    
    return {"sexo": model_name, "message": "Vuser é estranho"}




