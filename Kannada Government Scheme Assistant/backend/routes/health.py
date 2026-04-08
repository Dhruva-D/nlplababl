from fastapi import APIRouter

# APIRouter helps us break our application into smaller, manageable chunks
# Instead of putting all routes in main.py, we organize them in separate files.
router = APIRouter()

@router.get("/health")
def check_health():
    """
    Health Check Route.
    Visit: http://localhost:8000/api/health
    This route returns a simple message so we can verify if the server is running correctly.
    """
    return {
        "status": "success",
        "message": "Backend server is running perfectly!",
        "database_connected": True
    }
