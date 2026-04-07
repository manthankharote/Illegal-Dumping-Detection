from fastapi import FastAPI
from ai_service.garbage_env import GarbageDetectionEnv

app = FastAPI()
env = GarbageDetectionEnv()

@app.post("/reset")
def reset_env():
    return {"state": env.reset()}

@app.post("/step")
def step_env(req: dict):
    action = req.get("action", 0)
    state, reward, done, info = env.step(action)
    return {
        "state": state,
        "reward": float(reward),
        "done": bool(done),
        "info": info
    }

@app.get("/state")
def get_state():
    return {"state": env.state()}