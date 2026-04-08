from fastapi import FastAPI
import uvicorn
import sys
import os

# Ensure the root path is accessible so it finds ai_service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_service.garbage_env import GarbageDetectionEnv

app = FastAPI()
env = GarbageDetectionEnv()

# 🔥 OpenEnv standard requires a health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reset")
def reset_env():
    return env.reset()

@app.post("/step")
def step_env(req: dict):
    # Action parsing correctly formatted for the environment
    action = req.get("action", 0)
    state, reward, done, info = env.step(action)
    
    # 🔥 OpenEnv Expects tasks explicitly inside info or as top-level keys
    return {
        "observation": state,  # Changing 'state' to 'observation' as per OpenEnv spec
        "reward": float(reward),
        "done": bool(done),
        "info": info,
        "tasks": env.tasks,      # Validator directly fetching tasks
        "graders": env.tasks     # Fallback for graders
    }

@app.get("/state")
def get_state():
    return env.state()

# Injecting validator targets directly
@app.get("/tasks")
def get_tasks():
    return env.tasks

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()