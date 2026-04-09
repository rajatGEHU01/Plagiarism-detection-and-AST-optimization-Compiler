from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing the routers from the routes directory
from routes import plagiarism, optimizer

app = FastAPI(
    title="CodeLite++ AI Engine",
    description="AI-Based Plagiarism Detector and Code Optimizer for CodeLite++",
    version="1.0.0"
)

# ---------------------------------------------------------
# CORS (Cross-Origin Resource Sharing)
# This allows your index.html file to make requests to this 
# API even if they are hosted/opened from different places.
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, etc.
    allow_headers=["*"],
)

# -------------------------------
# Routes
# -------------------------------
# These connect the logic in routes/plagiarism.py and routes/optimizer.py
app.include_router(plagiarism.router, tags=["Plagiarism"])
app.include_router(optimizer.router, tags=["Optimizer"])


# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
def root():
    """
    Health check endpoint to verify the server is running.
    """
    return {
        "status": "online",
        "message": "CodeLite++ AI Engine is running 🚀"
    }

if __name__ == "__main__":
    import uvicorn
    # This allows you to run the file directly with 'python main.py'
    uvicorn.run(app, host="127.0.0.1", port=8000)