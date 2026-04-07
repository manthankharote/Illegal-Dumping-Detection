import os
import sys
import logging
import warnings
from contextlib import redirect_stdout, redirect_stderr

# Completely silence logging and warnings
logging.getLogger().setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore")

# Add ai-service to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_service'))

# Suppressing initial import/model prints and stderr to ensure strict log format
with open(os.devnull, 'w') as f, redirect_stdout(f), redirect_stderr(f):
    from ai_service.garbage_env import GarbageDetectionEnv

def main():
    print("[START]")
    
    # Supressing model loading initialization logs
    with open(os.devnull, 'w') as f, redirect_stdout(f), redirect_stderr(f):
        env = GarbageDetectionEnv()
        env.reset()
        
    # We will run 3 tasks with dummy actions: 
    # 1: detect garbage, 2: alert, 0: ignore
    dummy_actions = [1, 2, 0]
    
    for action in dummy_actions:
        # Suppressing YOLO inference and detector prints/errors
        with open(os.devnull, 'w') as f, redirect_stdout(f), redirect_stderr(f):
            next_state, reward, done, info = env.step(action)
            
        # Logging exactly as requested
        print(f"[STEP] action={action} reward={reward}")
        
    print("[END]")

if __name__ == "__main__":
    main()
