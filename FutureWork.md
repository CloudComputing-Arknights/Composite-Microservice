# Composite Microservice - FastAPI Project

## 📌 Overview
This project is a **Composite Microservice** built with **FastAPI** and **SQLModel/SQLAlchemy** following a clean layered architecture:


It integrates multiple domains — Items, Users, Transactions — and supports complex relationships such as Item-User bindings and Transaction participants.  
The service can interact with external microservices for validation and business logic.

---

## ✅ Current Implemented Endpoints

### **Addresses**
- `GET /addresses` – List all addresses  
- `POST /addresses` – Create a new address  
- `GET /addresses/{address_id}` – Get address by ID  
- `PATCH /addresses/{address_id}` – Update an address  
- `DELETE /addresses/{address_id}` – Delete an address  

### **Address-User**
- `POST /address-user/{address_id}/{user_id}` – Create binding between address and user  
- `GET /address-user/user/{user_id}` – List all addresses belonging to a specific user  
- `GET /address-user/address/{address_id}` – Get the owner (user) of a given address  
- `DELETE /address-user/{address_id}/{user_id}` – Delete binding between address and user

### **Item-Address**
- `POST /item-address/{item_id}/{address_id}` – Create binding between item and address  
- `DELETE /item-address/{item_id}/{address_id}` – Delete binding between item and address  
- `GET /item-address/address/{address_id}` – List all items located at a specific address  
- `GET /item-address/item/{item_id}` – Get address location of a specific item  

### **Items**
- `GET /items` – List all items  
- `POST /items` – Create a new item  
- `GET /items/{item_id}` – Get item by ID  
- `PATCH /items/{item_id}` – Update item  
- `DELETE /items/{item_id}` – Delete item  

### **Item-User**
- `POST /item-user/{item_id}/{user_id}` – Create binding between item and user  
- `GET /item-user/user/{user_id}` – List all items belonging to a specific user  
- `GET /item-user/item/{item_id}` – Get the owner (user) of a given item  
- `DELETE /item-user/{item_id}/{user_id}` – Delete binding between item and user  

### **Default (Generic / Auth)**
- `GET /` – Root welcome endpoint  
- `POST /token/sign-in` – Sign-in endpoint (returns auth token)  
- `GET /me/user` – Get authenticated user info  

### **Transactions**
- `GET /transactions` – List all transactions  
- `POST /transactions` – Create a transaction  
- `GET /transactions/{transaction_id}` – Get transaction by ID  
- `PATCH /transactions/{transaction_id}` – Update transaction  
- `DELETE /transactions/{transaction_id}` – Delete transaction  

### **Transaction-User-Item**
- `POST /transaction-user-item/{transaction_id}/{user_id}` – Create binding between transaction and user-item  
- `DELETE /transaction-user-item/{transaction_id}/{user_id}` – Delete binding between transaction and user-item  
- `GET /transaction-user-item` – List all transaction-user-item relations

<img width="2304" height="1542" alt="image" src="https://github.com/user-attachments/assets/4bf2fa23-a422-4c26-b42f-ba100c6361f4" />
<img width="2288" height="1820" alt="image" src="https://github.com/user-attachments/assets/7acbaa74-3188-436d-9fcd-209c1dd01b69" />
<img width="2296" height="1626" alt="image" src="https://github.com/user-attachments/assets/02ae52c5-7484-4d13-b53f-d87bd9aed0d5" />


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

