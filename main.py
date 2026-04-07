import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel

# Add ai_service to sys.path natively so garbage_env can import detector

from ai_service.garbage_env import GarbageDetectionEnv

app = FastAPI(title="Garbage Detection OpenEnv API")

# Initialize global environment
env = GarbageDetectionEnv()

# Action request schema
class ActionRequest(BaseModel):
    action: int

@app.post("/reset")
def reset_env():
    """Resets the environment."""
    state = env.reset()
    return {"state": state}

@app.post("/step")
def step_env(req: ActionRequest):
    """Executes a single step given an action (0, 1, or 2)."""
    state, reward, done, info = env.step(req.action)
    return {
        "state": state,
        "reward": float(reward),
        "done": done,
        "info": info
    }

@app.get("/state")
def get_state():
    """Returns the current environment state."""
    state = env.state()
    return {"state": state}
