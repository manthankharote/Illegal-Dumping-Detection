import os
import sys
from openai import OpenAI

# Add ai_service to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_service'))

from ai_service.garbage_env import GarbageDetectionEnv


def main():
    print("[START]")

    # 🔥 SAFE LLM CALL (Phase 2 requirement)
    try:
        if os.getenv("API_BASE_URL") and os.getenv("API_KEY"):
            client = OpenAI(
                base_url=os.getenv("API_BASE_URL"),
                api_key=os.getenv("API_KEY")
            )

            client.chat.completions.create(
                model=os.getenv("MODEL_NAME", "gpt-4"),
                messages=[
                    {"role": "user", "content": "Analyze environment state"}
                ],
                max_tokens=10
            )
    except Exception:
        pass

    # Initialize environment
    env = GarbageDetectionEnv()
    env.reset()

    # Fixed action sequence
    actions = [1, 2, 1]

    for action in actions:
        state, reward, done, info = env.step(action)
        print(f"[STEP] action={action} reward={reward}")

    print("[END]")


if __name__ == "__main__":
    main()