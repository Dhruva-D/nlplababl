from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. Import our modular routes and database connection
from routes.health import router as health_router
from routes.search import router as search_router
from database.database import get_database

# 2. Startup/shutdown lifecycle using modern FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup: connect to database
    get_database()
    yield
    # Runs on shutdown (nothing to clean up here)

# 3. Initialize the main FastAPI application
app = FastAPI(
    title="Kannada Government Scheme Assistant API",
    description="Backend API to serve scheme data to our React Frontend",
    lifespan=lifespan
)

# 3. Configure CORS (Cross-Origin Resource Sharing)
# React (Vite) usually runs on http://localhost:5173. 
# We need to tell our FastAPI server to allow requests from the React frontend.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Domains allowed to connect to this API
    allow_credentials=True,      # Allow cookies and credentials
    allow_methods=["*"],         # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],         # Allow all headers
)


# 5. Connect our modular routes
# We include the 'health' route we created and prefix it with '/api'
app.include_router(health_router, prefix="/api", tags=["Health Checks"])
app.include_router(search_router, prefix="/api", tags=["Search API"])


# 6. A friendly root route 
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Kannada Government Scheme Assistant API",
        "hint": "Go to http://localhost:8000/docs to see the interactive API documentation!"
    }
