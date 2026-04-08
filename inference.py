import json
import os
from openai import OpenAI
from ai_service.garbage_env import GarbageDetectionEnv


def main():
    print("[START]")

    base_url = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")

    if base_url and api_key:
        try:
            client = OpenAI(
                base_url=base_url,
                api_key=api_key
            )

            client.chat.completions.create(
                model=os.environ.get("MODEL_NAME", "gpt-4"),
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )

            print("[LLM CALL SUCCESS]")

        except Exception as e:
            print(f"[LLM ERROR] {e}")

    env = GarbageDetectionEnv()
    env.reset()

    actions = [1, 2, 1]

    tasks = {
        "task_easy": 0.3,
        "task_medium": 0.6,
        "task_hard": 0.8
    }

    for action in actions:
        state, reward, done, info = env.step(action)

        # 🔥 PERFECT JSON FORMAT
        print(
            f"[STEP] action={action} reward={reward} tasks={json.dumps(tasks)}"
        )

    print("[END]")


if __name__ == "__main__":
    main()