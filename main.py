from fastapi import FastAPI
from pydantic import BaseModel
from ai_service.garbage_env import GarbageDetectionEnv

app = FastAPI()

env = GarbageDetectionEnv()

class ActionRequest(BaseModel):
    action: int

@app.post("/reset")
def reset_env():
    state = env.reset()
    return {"state": state}

@app.post("/step")
def step_env(req: ActionRequest):
    state, reward, done, info = env.step(req.action)
    return {
        "state": state,
        "reward": float(reward),
        "done": bool(done),
        "info": info
    }

@app.get("/state")
def get_state():
    return {"state": env.state()}