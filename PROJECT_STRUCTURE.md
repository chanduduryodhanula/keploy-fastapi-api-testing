# Project Structure

```
keploy-project/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── database.py              # MongoDB connection and configuration
│   ├── models.py                # Pydantic schemas (UserCreate, UserUpdate, UserResponse)
│   └── routers/
│       ├── __init__.py          # Router package initialization
│       └── users.py             # User CRUD API routes
├── scripts/
│   ├── keploy-record.sh         # Linux/Mac script for Keploy recording
│   ├── keploy-record.bat        # Windows script for Keploy recording
│   ├── keploy-test.sh           # Linux/Mac script for Keploy testing
│   └── keploy-test.bat          # Windows script for Keploy testing
├── tests/                       # Keploy generated tests (auto-created)
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image configuration
├── docker-compose.yml           # Docker Compose setup (includes MongoDB)
├── keploy-config.yaml           # Keploy configuration file
├── .dockerignore                # Docker ignore patterns
├── .gitignore                   # Git ignore patterns
├── README.md                    # Comprehensive project documentation
└── PROJECT_STRUCTURE.md         # This file

```

## Key Files

### Application Files
- `app/main.py` - FastAPI app with startup/shutdown handlers, CORS middleware
- `app/database.py` - MongoDB async connection management
- `app/models.py` - Pydantic models for request/response validation
- `app/routers/users.py` - Complete CRUD operations for User entity

### Configuration Files
- `requirements.txt` - All Python dependencies
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Multi-container setup (API + MongoDB)
- `keploy-config.yaml` - Keploy test recording/replay configuration

### Documentation
- `README.md` - Complete setup and usage guide
