# User Management REST API with Automated Test Generation using Keploy

A production-ready FastAPI application that provides CRUD operations for user management, integrated with Keploy for automated test case generation and replay capabilities.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Keploy Integration](#keploy-integration)
- [Docker Deployment](#docker-deployment)
- [Testing](#testing)
- [Developer Experience Improvements](#developer-experience-improvements)

## 🎯 Project Overview

This project demonstrates a modern backend API built with FastAPI, MongoDB, and Keploy. It showcases:

- **RESTful API design** with proper HTTP status codes and error handling
- **Database persistence** using MongoDB
- **Automated test generation** using Keploy to record API traffic and generate test cases
- **Containerized deployment** with Docker for easy setup and distribution

## 🛠 Tech Stack

- **Python 3.10+** - Programming language
- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - NoSQL database for data persistence
- **Motor** - Async MongoDB driver for Python
- **Pydantic** - Data validation using Python type annotations
- **Keploy** - API testing platform for automated test generation
- **Docker** - Containerization platform
- **Uvicorn** - ASGI server

## ✨ Features

- ✅ Complete CRUD operations for User entity
- ✅ UUID-based user identification
- ✅ Email validation and duplicate prevention
- ✅ Input validation with meaningful error messages
- ✅ Comprehensive error handling for edge cases
- ✅ Automatic test generation using Keploy
- ✅ Docker support for easy deployment
- ✅ Async/await support for better performance
- ✅ OpenAPI/Swagger documentation

## 📡 API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/` | Root endpoint with API information | 200 |
| `GET` | `/health` | Health check endpoint | 200 |
| `POST` | `/api/users` | Create a new user | 201, 400, 500 |
| `GET` | `/api/users` | Get all users | 200, 500 |
| `GET` | `/api/users/{user_id}` | Get user by ID | 200, 400, 404, 500 |
| `PUT` | `/api/users/{user_id}` | Update user by ID | 200, 400, 404, 500 |
| `DELETE` | `/api/users/{user_id}` | Delete user by ID | 204, 400, 404, 500 |

### User Entity Schema

```json
{
  "user_id": "uuid",
  "name": "string (1-100 chars)",
  "email": "valid email address",
  "age": "integer (1-150)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Example Request/Response

**Create User:**
```bash
POST /api/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30
}
```

**Response (201 Created):**
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## 📁 Project Structure

```
keploy-project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # MongoDB connection setup
│   ├── models.py            # Pydantic schemas
│   └── routers/
│       ├── __init__.py
│       └── users.py         # User CRUD routes
├── tests/                   # Keploy generated tests (auto-created)
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose setup
├── keploy-config.yaml      # Keploy configuration
├── .dockerignore
├── .gitignore
└── README.md
```

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **MongoDB** - Either:
  - Local MongoDB installation ([Download MongoDB](https://www.mongodb.com/try/download/community))
  - MongoDB Atlas account (free tier available)
- **Docker** (optional, for containerized deployment) - [Download Docker](https://www.docker.com/get-started)
- **Keploy** - [Install Keploy](https://docs.keploy.io/docs/server/introduction/)

## 🚀 Installation & Setup

### 1. Clone or Navigate to Project Directory

```bash
cd "keploy project"
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables (Optional)

Create a `.env` file or export environment variables:

```bash
# .env file
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=user_management
PORT=8000
```

Or set them directly:

```bash
# Windows PowerShell
$env:MONGODB_URL="mongodb://localhost:27017"
$env:DATABASE_NAME="user_management"
$env:PORT="8000"

# Linux/Mac
export MONGODB_URL=mongodb://localhost:27017
export DATABASE_NAME=user_management
export PORT=8000
```

### 5. Start MongoDB

**Option A: Local MongoDB**
```bash
# Windows (if installed as service, it starts automatically)
# Or manually:
mongod

# Linux/Mac
sudo systemctl start mongod
# Or:
mongod --dbpath /path/to/data
```

**Option B: MongoDB Atlas**
- Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Get your connection string and update `MONGODB_URL`

## ▶️ Running the Application

### Method 1: Using Uvicorn Directly

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Method 2: Using Python Module

```bash
python -m app.main
```

### Method 3: Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

This will start both MongoDB and the FastAPI application.

## 🔧 Keploy Integration

Keploy automatically records API traffic and generates test cases that can be replayed later.

### Installing Keploy

**Linux/Mac:**
```bash
curl -O https://github.com/keploy/keploy/releases/latest/download/keploy_linux_amd64.tar.gz
tar -xzf keploy_linux_amd64.tar.gz
sudo mv keploy /usr/local/bin/
```

**Windows:**
Download from [Keploy Releases](https://github.com/keploy/keploy/releases) and add to PATH.

**Or using package managers:**
```bash
# Homebrew (Mac)
brew install keploy

# Scoop (Windows)
scoop install keploy
```

### Keploy Setup

1. **Start Keploy Server** (in a separate terminal):

```bash
keploy
```

Keploy server will start on `http://localhost:8081` by default.

2. **Record API Traffic**

In one terminal, start your FastAPI application:

```bash
# Make sure Keploy is running first
# Then start your app through Keploy proxy
keploy record -c "uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

Or if using Docker:

```bash
keploy record -c "docker-compose up"
```

3. **Generate Test Traffic**

While the app is running with Keploy record mode, make API calls:

```bash
# Create a user
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'

# Get all users
curl http://localhost:8080/api/users

# Get user by ID (replace with actual ID)
curl http://localhost:8080/api/users/{user_id}

# Update user
curl -X PUT http://localhost:8080/api/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "age": 31}'

# Delete user
curl -X DELETE http://localhost:8080/api/users/{user_id}
```

**Note:** Use port `8080` (Keploy proxy) instead of `8000` when recording.

4. **Stop Recording**

Press `Ctrl+C` to stop recording. Keploy will save the test cases in the `tests/` directory.

5. **Replay Tests**

To replay the recorded tests:

```bash
# Start Keploy server (if not running)
keploy

# In another terminal, start your app
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Replay tests
keploy test -c "echo 'App is running'" --delay 10
```

Or use the test command directly:

```bash
keploy test --config keploy-config.yaml
```

### Keploy Configuration

The `keploy-config.yaml` file contains Keploy settings:

- **App Configuration**: App name, port, command, and proxy port
- **Server URL**: Keploy server endpoint
- **Test Filters**: Noise filters to ignore dynamic fields (timestamps, UUIDs)
- **Test Timeout**: Maximum time for test execution

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t user-management-api .
```

### Run Container

```bash
# Make sure MongoDB is running or use docker-compose
docker run -p 8000:8000 \
  -e MONGODB_URL=mongodb://host.docker.internal:27017 \
  -e DATABASE_NAME=user_management \
  user-management-api
```

### Using Docker Compose (Includes MongoDB)

```bash
# Start services
docker-compose up --build

# Start in detached mode
docker-compose up -d --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f api
```

## 🧪 Testing

### Manual Testing

Use the Swagger UI at http://localhost:8000/docs to interactively test all endpoints.

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Create user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Smith", "email": "alice@example.com", "age": 25}'

# Get all users
curl http://localhost:8000/api/users

# Get user by ID
curl http://localhost:8000/api/users/{user_id}

# Update user
curl -X PUT http://localhost:8000/api/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "age": 26}'

# Delete user
curl -X DELETE http://localhost:8000/api/users/{user_id}
```

### Edge Cases Handled

- ✅ **Duplicate Email**: Returns 400 Bad Request
- ✅ **Invalid User ID**: Returns 400 Bad Request for invalid UUID format
- ✅ **User Not Found**: Returns 404 Not Found
- ✅ **Invalid Input**: Returns 400 Bad Request with validation errors
- ✅ **Empty Update**: Returns 400 Bad Request if no fields provided

## 💡 Developer Experience Improvements

This project improves developer experience through:

1. **Automated Test Generation**
   - Keploy records real API traffic automatically
   - No need to manually write test cases
   - Tests are generated from actual usage patterns

2. **Zero-Configuration Setup**
   - Docker Compose for one-command deployment
   - Environment variables for easy configuration
   - Clear project structure

3. **Comprehensive Documentation**
   - OpenAPI/Swagger UI for interactive API exploration
   - ReDoc for beautiful API documentation
   - Detailed README with examples

4. **Type Safety**
   - Pydantic models ensure data validation
   - Type hints throughout the codebase
   - IDE autocomplete support

5. **Error Handling**
   - Meaningful error messages
   - Proper HTTP status codes
   - Detailed error responses

6. **Development Workflow**
   - Hot reload with `--reload` flag
   - Clear logging and debugging information
   - Easy MongoDB connection management

7. **Production Ready**
   - Async/await for better performance
   - CORS middleware configuration
   - Health check endpoints
   - Docker support for deployment

## 📝 Notes

- The `tests/` directory will be automatically created by Keploy when recording tests
- Make sure MongoDB is running before starting the FastAPI application
- When using Keploy, use port `8080` (proxy) instead of `8000` (direct)
- Timestamps and UUIDs are filtered in Keploy tests to avoid flaky tests
- All user IDs are UUIDs for better uniqueness and security

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements.

## 📄 License

This project is open source and available for educational purposes.

---

**Built with ❤️ using FastAPI, MongoDB, and Keploy**
