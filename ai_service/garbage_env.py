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

        tasks = {
            "task_easy": 0.3,
            "task_medium": 0.6,
            "task_hard": 0.8
        }

        return (
            {"step": self.current_step},
            0.5,
            self.current_step >= 3,
            {"tasks": tasks}
        )