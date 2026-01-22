from fastapi import FastAPI

app = FastAPI(title="PDF Screening API")

@app.get("/")
def health_check():
    return {"status": "API running successfully"}
