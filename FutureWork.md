# Composite Microservice - FastAPI Project

## 📌 Overview
This project is a **Composite Microservice** built with **FastAPI** and **SQLModel/SQLAlchemy** following a clean layered architecture:


It integrates multiple domains — Items, Users, Transactions — and supports complex relationships such as Item-User bindings and Transaction participants.  
The service can interact with external microservices for validation and business logic.

---

## ✅ Current Implemented Endpoints

### **Item Service**
- `POST /items` – Create an item  
- `GET /items/{item_id}` – Retrieve item details by ID  
- `GET /items` – List all items  
- `PUT /items/{item_id}` – Update an item  
- `DELETE /items/{item_id}` – Delete an item

### **User Service**
- `POST /users` – Create a user  
- `GET /users/{user_id}` – Retrieve user details by ID  
- `GET /users` – List all users  
- `PUT /users/{user_id}` – Update a user  
- `DELETE /users/{user_id}` – Delete a user

### **Item-User Relationship Service**
- `POST /item-user` – Create an item-user binding  
- `GET /item-user/{user_id}` – List all items for a user  
- `GET /item-user/owner/{item_id}` – Find the owner of an item  
- `DELETE /item-user/{item_id}?user_id=X` – Remove an item-user binding  
- *(Optional)* `GET /item-user/verify/{item_id}?user_id=X` – Verify item ownership

### **Transaction Service**
- `POST /transactions` – Create a transaction  
- `GET /transactions/{transaction_id}` – Retrieve transaction details  
- `GET /transactions` – List all transactions  
- `PUT /transactions/{transaction_id}` – Update a transaction  
- `DELETE /transactions/{transaction_id}` – Delete a transaction

---

## 🔮 Future Work: Migration to DTO & PO

Currently, the project uses:
- `schemas/` – legacy request/response models (only 3 files)
- `models/dto/` – full set of API models (Pydantic)
- `models/po/` – database models (ORM)

### **Goal**  
Unify and simplify:  
- **All API data models** → `models/dto`  
- **All database mappings** → `models/po`  
- Remove `schemas/` entirely after migration.

### **Migration Strategy**
1. **Bridge Phase**  
   - Modify each schema file to re-export DTO classes from `models/dto`:
     ```python
     # app/schemas/item.py
     from app.models.dto.item_dto import ItemCreate, ItemUpdate, ItemResponse
     ```
   - This keeps old imports working while using new DTOs.

2. **Refactor Imports**  
   - Gradually change routers and services to import directly from `models/dto`.

3. **Remove `schemas/`**  
   - Once all imports are updated and tested, delete the schemas directory.

4. **Complete PO models**  
   - Ensure ORM definitions exist for all entities in `models/po`.

---

## 🛠 Final Composite Microservice Structure (After Migration)
## 🗂 Composite Microservice Architecture

```plaintext
+----------------------------+
|        Client (HTTP)       |
+----------------------------+
              |
              v
+----------------------------+
| API Router (resources/)    |
| - Defines endpoints        |
| - Parses params & body     |
| - Uses DTO for validation  |
+----------------------------+
              |
              v
+----------------------------+
| Service Layer (services/)  |
| - Business logic           |
| - Calls external services  |
| - Transforms DTO to PO     |
+----------------------------+
              |
              v
+----------------------------+
| Repository Layer           |
| (repositories/)            |
| - CRUD operations          |
| - Uses PO ORM models       |
+----------------------------+
              |
              v
+----------------------------+
| Persistent Objects (PO)    |
| (models/po/)               |
| - ORM table mappings       |
+----------------------------+
              |
              v
+----------------------------+
| Database (MySQL/PostgreSQL)|
+----------------------------+

```
---

## 📂 Data Model Roles

- **DTO (`models/dto`)**
  - Pydantic API request/response models
  - Validates input & serializes output
- **PO (`models/po`)**
  - SQLModel/SQLAlchemy ORM models
  - Maps directly to database tables

---

## 🎯 Benefits of This Architecture

1. **Separation of concerns** — API payload vs persistence logic.
2. **Consistency** — One place for API models, one for DB models.
3. **Maintainability** — Database changes require minimal impact to API layers.
4. **Extensibility** — Adding new entity = DTO + PO + repository + service + router.

