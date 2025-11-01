# Composite-Microservice

Here is a concise list of all implemented endpoints:

* **`GET /`**: Root endpoint to confirm the API is running.
* **`GET /posts`**: Performs **asynchronous aggregation** (Stateless) to fetch all items and enrich them with user data.
* **`POST /trades`**: A placeholder endpoint (returns `501`) that demonstrates the **architectural block** (ID mismatch) requiring a DBaaS.
* **`GET /users/{user_id}/trades`**: A placeholder endpoint (returns `501`) that also demonstrates the DBaaS requirement.
* **`GET /users/{user_id}/profile`**: A placeholder (returns `501`) for the future **Stateful (DBaaS) endpoint** from your professor's slides.
* **`POST /reports`**: Implements **`202 Accepted`** by using **background threads** for a long-running synchronous task.
* **`PUT /items-concurrency-demo/{item_id}`**: Implements ETag concurrency checks, returning **`412 Precondition Failed`** and **`428 Precondition Required`**.
* **`POST /demo-create`**: A simple endpoint that demonstrates a successful **`201 Created`** response.
* **`GET /force-error`**: A test endpoint that triggers a bug to demonstrate the **`500 Internal Server Error`** handler.
