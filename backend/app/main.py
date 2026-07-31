from fastapi import FastAPI

app = FastAPI(
    title="CricketGPT OS",
    version="1.0.0",
    description="AI-powered Cricket Analytics Platform"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to CricketGPT OS 🚀"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "project": "CricketGPT OS"
    }