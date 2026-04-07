from fastapi import FastAPI, Request
from pydantic import BaseModel
from ai_service.garbage_env import GarbageDetectionEnv

app = FastAPI()

env = GarbageDetectionEnv()

class ActionRequest(BaseModel):
    action: int

@app.post("/reset")
async def reset_env(request: Request):
    state = env.reset()
    return {
        "state": state,
        "info": {}
    }

@app.post("/step")
async def step_env(req: ActionRequest):
    state, reward, done, info = env.step(req.action)
    return {
        "state": state,
        "reward": float(reward),
        "done": bool(done),
        "info": info if info else {}
    }

@app.get("/state")
async def get_state():
    return {
        "state": env.state()
    }