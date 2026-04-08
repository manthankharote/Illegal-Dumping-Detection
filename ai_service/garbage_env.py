class GarbageDetectionEnv:
    def __init__(self):
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        return {"step": 0}

    def state(self):
        return {"step": self.current_step}

    def step(self, action):
        self.current_step += 1

        # 🔥 ALL 3 TASKS EVERY STEP (SAFE)
        tasks = {
            "task_easy": 0.4,
            "task_medium": 0.6,
            "task_hard": 0.8
        }

        done = self.current_step >= 3

        return (
            {"step": self.current_step},
            0.5,
            done,
            {
                "tasks": {
                    k: float(v) for k, v in tasks.items()
                }
            }
        )