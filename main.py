from fastapi import FastAPI

# Create FastAPI app
app = FastAPI(title="St. John's Weather Alert System")

# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to St. John's Weather Alert System",
        "status": "running",
        "location": "St. John's, NL, Canada"
    }

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}