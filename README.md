# Pokémon API
A FastAPI-based REST API for managing Pokémon, types, and their relationships.

## 📌 Overview
Pokémon API is a RESTful backend service built with FastAPI and SQLAlchemy.
It models Pokémon, their types, and relationships using a scalable relational schema.

## ✨ Features
- CRUD operations for Pokémon and Types
- Support for single and dual-type Pokémon
- Ordered type slots (primary / secondary)
- Clean many-to-many relationship modeling

## ⚙️ Tech Stack
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

## 🗄️ Database Structure
- pokemons
- types
- pokemon_types (association table)


## 🗺️ Entity Relationship Diagram (ERD)

```
+-------------+        +------------------+        +-------------+
|  pokemons   |        |  pokemon_types   |        |   types     |
+-------------+        +------------------+        +-------------+
| PK id       |<-------| PK pokemon_id FK |  +---> | PK id       |
| name        |        | PK type_id FK    |--+     | name        |
| height      |        | slot             |        +-------------+
| weight      |        |                  |
| category    |        +------------------+
| description |
+-------------+

```



## 🔌 API Endpoints

### Pokémon
- GET /pokemons
- GET /pokemons/{id}
- GET /pokemons/name/{name}
- GET /pokemons/type/{type_name}
- POST /pokemons
- PUT /pokemons/{id}
- DELETE /pokemons/{id}

### Types
- GET /types
- GET /types/{id}
- POST /types
- PUT /types/{id}
- DELETE /types/{id}


## 📂 Project Structure
```
Pokemon/
├── app/
│   ├── alembic/
│   ├── core/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── alembic.ini
│   └── main.py
├── pokemon.db
├── README.md
└── requirements.txt
```

## 🚀 Setup & Installation
```bash
git clone https://github.com/yourusername/pokemon-api.git
cd Pokemon
pip install -r requirements.txt
uvicorn app.main:app --reload
```
