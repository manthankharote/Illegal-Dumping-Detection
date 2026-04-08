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

        return (
            {"step": self.current_step},
            0.7,   # safe reward
            False,
            {
                "task_scores": {
                    "task_easy": 0.6,
                    "task_medium": 0.7,
                    "task_hard": 0.8
                }
            }
        )