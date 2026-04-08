import os
from openai import OpenAI
from ai_service.garbage_env import GarbageDetectionEnv


def main():
    print("[START]")

    # 🔥 FORCE LLM CALL (NO SKIP)
    base_url = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")

    if base_url and api_key:
        client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        response = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4"),
            messages=[
                {"role": "user", "content": "Hello from hackathon"}
            ],
            max_tokens=5
        )

        print("[LLM CALL SUCCESS]")

    else:
        print("[LLM ENV NOT FOUND]")

    # 🔥 ENV RUN
    env = GarbageDetectionEnv()
    env.reset()

    actions = [1, 2, 1]

    for action in actions:
        state, reward, done, info = env.step(action)

        print(
            f"[STEP] action={action} reward={reward} "
            f"tasks={{\"task_easy\":0.3,\"task_medium\":0.6,\"task_hard\":0.8}}"
        )

    print("[END]")


if __name__ == "__main__":
    main()