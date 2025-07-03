
# FastAPI Redis Caching API

A high-performance FastAPI project with Redis caching implemented for optimizing frequent API requests like `/users`.

---

## Features

- ✅ Built with FastAPI
- ✅ Redis caching for user data
- ✅ Automatic cache invalidation on update or create
- ✅ Performance tracking with response time
- ✅ Swagger UI for testing
- ✅ Custom HTML homepage with API navigation

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/jwt_redis_project.git
cd jwt_redis_project
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn redis pydantic
```

### 3. Start Redis Server

If Redis is installed locally on Windows:
```bash
cd path/to/Redis-x64-3.0.504
.
edis-server.exe
```

Ensure Redis is running on port `6379`.

---

## Run the API
```bash
uvicorn main:app --reload
```

---

## API Endpoints

| Method | Endpoint         | Description              |
|--------|------------------|--------------------------|
| GET    | `/`              | Welcome page with links  |
| GET    | `/users`         | Get all users (cached)   |
| PUT    | `/users/{id}`    | Update a user            |
| POST   | `/users`         | Add a new user           |
| GET    | `/docs`          | Swagger API documentation |

---

## Cache Behavior

- Users list is cached in Redis for `60 seconds`
- Cache is automatically invalidated when:
  - A new user is added (`POST`)
  - A user is updated (`PUT`)
- If cache is valid → response is served from Redis

---

## Screenshots

> Optionally add screenshots of the Swagger UI and HTML homepage.

---

## Author

**Netika**  
Developer with experience in building APIs using FastAPI and implementing performance optimizations using Redis.

---

## Feedback

If you find this project useful, consider giving it a star or sharing your feedback.
