from fastapi import FastAPI
from pydantic import BaseModel
from ai_service.garbage_env import GarbageDetectionEnv

app = FastAPI()

env = GarbageDetectionEnv()

class ActionRequest(BaseModel):
    action: int

@app.get("/")
def root():
    return {"message": "API running"}

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(req: ActionRequest):
    state, reward, done, info = env.step(req.action)

    return {
        "state": state,
        "reward": reward,
        "done": done,
        "tasks": info.get("tasks", {})
    }