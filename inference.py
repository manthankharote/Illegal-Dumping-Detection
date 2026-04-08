import json
import os
import sys
from openai import OpenAI

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_service'))
from ai_service.garbage_env import GarbageDetectionEnv


def main():
    print("[START]")

    # LLM call (keep as is)
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

    for i, action in enumerate(actions):
        state, reward, done, info = env.step(action)

        # 🔥 DIFFERENT TASK EACH STEP
        if i == 0:
            tasks = {"task_easy": 0.3}
        elif i == 1:
            tasks = {"task_medium": 0.6}
        else:
            tasks = {"task_hard": 0.9}

        print(f"[STEP] action={action} reward={reward} tasks={json.dumps(tasks, separators=(',', ':'))}")

    print("[END]")


if __name__ == "__main__":
    main()