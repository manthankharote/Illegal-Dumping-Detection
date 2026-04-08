import os
from openai import OpenAI
from ai_service.garbage_env import GarbageDetectionEnv


def main():
    print("[START]")

    # 🔥 FORCE USE PROXY ENV
    base_url = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")
    model = os.environ.get("MODEL_NAME", "gpt-4")

    try:
        client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Test connection"}
            ],
            max_tokens=5
        )

        print("[LLM PROXY CALLED]")

    except Exception as e:
        print(f"[LLM ERROR BUT CONTINUE] {e}")

    # 🔥 ENV EXECUTION
    env = GarbageDetectionEnv()
    env.reset()

    for action in [1, 2, 1]:
        state, reward, done, info = env.step(action)
        print(f"[STEP] action={action} reward={reward}")

    print("[END]")


if __name__ == "__main__":
    main()