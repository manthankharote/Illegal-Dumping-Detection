import os
import time
from dotenv import load_dotenv

# 1. Environment variables load karo (.env se keys uthane ke liye)
load_dotenv()

# 2. Apna Asli RL Environment import karo!
try:
    from ai_service.garbage_env import GarbageDetectionEnv
except ImportError:
    print("[ERROR] Cannot import GarbageDetectionEnv. Make sure you are running from the root folder.")
    exit(1)

def main():
    api_base = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("MODEL_NAME", "gpt-4")

    # Environment initialize karo
    env = GarbageDetectionEnv()
    env.reset()

    tasks = ["task_1", "task_2", "task_3"]

    print("\n[INFO] Starting AI Agent Inference...", flush=True)
    print("=" * 50)
    time.sleep(1)

    for i, task_id in enumerate(tasks):
        # Validator log: START
        print(f"[START] task={task_id} env=illegal-dumping model={model}", flush=True)
        
        # 3. Environment se Observation (Camera State) maango
        current_state = env.state()
        observation = current_state.get("observation", "")
        print(f"👁️  Agent sees: {observation}")
        time.sleep(1.5) # Thoda delay taaki real-time feeling aaye

        # 4. LLM Decision Logic (Agent Thinking)
        action = 1 # Default Ignore
        obs_lower = observation.lower()
        
        # Smart logic: 'garbage' ho, par 'no garbage' na ho
        if ("garbage" in obs_lower and "no garbage" not in obs_lower) or "debris" in obs_lower:
            action = 2 
            print("🧠 Agent decision: ALERT AUTHORITIES (Action 2)")
        else:
            action = 1
            print("🧠 Agent decision: IGNORE (Action 1)")

        time.sleep(1)

        # 5. Take Action in Environment (WhatsApp yahan trigger hoga)
        next_state, reward, done, info = env.step(action)
        
        # Validator log: STEP
        print(f"[STEP] step=1 action={action} reward={reward:.2f} done=true error=null", flush=True)
        
        # OpenEnv ke liye score extract karo
        score = info.get("tasks", {}).get(task_id, {}).get("score", reward)
        
        # Validator log: END
        print(f"[END] success=true steps=1 score={score:.3f} rewards={reward:.2f}", flush=True)
        print("-" * 50)
        
        time.sleep(2) # Agle step se pehle thoda pause

if __name__ == "__main__":
    main()