from fastapi import FastAPI
import subprocess
import sys

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/run-pipeline")
def run_pipeline():

    subprocess.Popen(
        [sys.executable, "run_pipeline.py"]
    )

    return {
        "success": True,
        "message": "Pipeline started in background"
    }