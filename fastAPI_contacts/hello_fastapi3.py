# EXERCÍCIO: 
#     2. Fazer "hello_fastapi3.py" com:
#         2.1 Guardar os contactos num lista em memória e inicializar com 3 contactos

#         2.2 Operações para:
#             . obter um contacto pelo email_addr
#             . alterar um contacto localizado pelo email_addr (PUT)
#             - acrescentar novo contacto (POST)

#         2.3 Redefinir 2.1 para ler contactos a partir de ficheiro JSON

from datetime import datetime
import json
from typing import Iterable
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class Contact(BaseModel):
    id: int = Field(gt = 10_000, lt=99_999, frozen = True)
    name: str = Field(min_length = 1, frozen = True)
    email_addr: EmailStr = Field(pattern = r'.+@mail\.com')
    last_changed: datetime = datetime.now()
    available: bool | None = None    
#:

file_path ='contacts.json'

def save_contacts(file_path: str, contacts: Iterable[Contact]):
    with open(file_path, 'wt') as file:
        data = [contact.model_dump() for contact in contacts]
        json.dump(data, file, default=str)
#:

def load_contacts(file_path: str):
    with open(file_path, 'rt') as file:
        data = json.load(file)
        return [Contact(**obj) for obj in data]
#:

contacts = load_contacts(file_path)

@app.get('/contact/list')
async def list_contacts():
    return contacts
#:

@app.get('/contact/id/{id}')
async def get_contact_by_id(contact_id: int):
    for contact in contacts:
        if contact_id == contact.id:
            return contact
    return None 
#:


@app.get('/contact/email/{email_addr}')
async def get_contact_by_email(email_addr: str):
    for contact in contacts:
        if email_addr == contact.email_addr:
            return contact
    return None 
#:


class NewEmailAddr(BaseModel):
    new_email_addr: EmailStr = Field(pattern = r'.+@mail\.com')
#:

@app.put('/contact/updatecontact/{email_addr}')
async def update_contact(email_addr: str, new_email_req:NewEmailAddr, available: bool):
    for contact in contacts:    
        if email_addr == contact.email_addr:
            contact.email_addr = new_email_req.new_email_addr
            contact.available = available
            contact.last_changed = datetime.now()
    return None
#:

@app.post('/contact/addcontact')
async def add_contact(new_contact: Contact):
    contacts.append(new_contact)
    return new_contact
#:

@app.post('/contact/saveall')
async def save_all_contacts():
    save_contacts(file_path, contacts)
#:

