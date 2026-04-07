from fastapi import FastAPI
import uvicorn
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

# 🔥 REQUIRED MAIN FUNCTION
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

# 🔥 REQUIRED ENTRYPOINT
if __name__ == "__main__":
    main()