from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/reset")
def reset():
    try:
        output = subprocess.check_output(["python", "inference.py"], text=True)
        print(output)
    except Exception as e:
        print("Error:", e)

    return {"status": "reset done"}