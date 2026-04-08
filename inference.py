import os
import sys
import json
from openai import OpenAI

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_service'))
from ai_service.garbage_env import GarbageDetectionEnv


def main():
    print("[START]")

    # LLM (required for Phase 2)
    try:
        if os.getenv("API_BASE_URL") and os.getenv("API_KEY"):
            client = OpenAI(
                base_url=os.getenv("API_BASE_URL"),
                api_key=os.getenv("API_KEY")
            )

            client.chat.completions.create(
                model=os.getenv("MODEL_NAME", "gpt-4"),
                messages=[{"role": "user", "content": "Analyze"}],
                max_tokens=5
            )
    except:
        pass

    env = GarbageDetectionEnv()
    env.reset()

    actions = [1, 2, 1]

    for action in actions:
        state, reward, done, info = env.step(action)

        # 🔥 CRITICAL: PRINT TASKS
        tasks = state.get("tasks", {})

        print(f"[STEP] action={action} reward={reward} tasks={tasks}")

    print("[END]")


if __name__ == "__main__":
    main()