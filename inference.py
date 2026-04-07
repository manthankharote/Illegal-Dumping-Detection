import sys
import os

# Add ai_service to sys.path natively
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_service'))

from ai_service.garbage_env import GarbageDetectionEnv

def main():
    print("[START]")
    
    env = GarbageDetectionEnv()
    env.reset()
    
    dummy_actions = [1, 2, 0]
    
    for action in dummy_actions:
        next_state, reward, done, info = env.step(action)
        print(f"[STEP] action={action} reward={reward}")
        
    print("[END]")

if __name__ == "__main__":
    main()
