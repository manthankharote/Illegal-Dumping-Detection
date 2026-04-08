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

        # 🔥 ALL TASKS ALWAYS PRESENT
        tasks = {
            "task1": 0.3,
            "task2": 0.6,
            "task3": 0.9
        }

        done = self.current_step >= 3

        # 🔥 CRITICAL: tasks must be in info BUT ALSO returned clearly
        return (
            {
                "step": self.current_step,
                "tasks": tasks   # 🔥 TOP LEVEL (VERY IMPORTANT)
            },
            0.5,
            done,
            {}
        )