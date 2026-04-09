from fastapi import FastAPI
import uvicorn
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_service.garbage_env import GarbageDetectionEnv

app = FastAPI()
env = GarbageDetectionEnv()

@app.post("/reset")
def reset_env():
    return env.reset()

@app.post("/step")
def step_env(req: dict):
    action = req.get("action", 1)
    obs, reward, done, info = env.step(action)
    
    # EXACT OpenEnv JSON format. Nothing extra.
    return {
        "observation": obs,
        "reward": float(reward),
        "done": bool(done),
        "info": info
    }

@app.get("/state")
def get_state():
    return env.state()

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()