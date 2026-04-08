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
            "task1": 0.3,
            "task2": 0.6,
            "task3": 0.8
        }

        done = self.current_step >= 3

        return (
            {"step": self.current_step, "tasks": tasks},
            0.5,
            done,
            {}
        )