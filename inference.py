from ai_service.garbage_env import GarbageDetectionEnv

def main():
    print("[START]")

    env = GarbageDetectionEnv()
    env.reset()

    actions = [1, 2, 1]

    for action in actions:
        state, reward, done, info = env.step(action)
        print(f"[STEP] action={action} reward={reward}")

    print("[END]")


if __name__ == "__main__":
    main()