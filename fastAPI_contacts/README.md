# FastAPI Contacts Management

This project is a simple contacts management API built with FastAPI. It allows users to manage a list of contacts stored in a JSON file.

## Features
- List all contacts
- Get a contact by ID
- Get a contact by email
- Update a contact's email and availability
- Add a new contact
- Save all contacts to a JSON file

## Requirements
- Python
- FastAPI
- Pydantic

## Installation
1. Clone the repository and navigate to the project folder:
```bash
git clone https://github.com/raquelmarques1995/python_projects.git
cd python_projects/fastapi_contacts
```

2. Install dependencies:
```bash
pip install fastapi pydantic
```

## Usage
1. Run the API server:
```bash
fastapi dev hello_fastapi3.py
```

## API Endpoints
- **GET** `/contact/list` - List all contacts
- **GET** `/contact/id/{id}` - Get a contact by ID
- **GET** `/contact/email/{email_addr}` - Get a contact by email
- **PUT** `/contact/updatecontact/{email_addr}` - Update a contact's email and availability
- **POST** `/contact/addcontact` - Add a new contact
- **POST** `/contact/saveall` - Save all contacts to the JSON file

