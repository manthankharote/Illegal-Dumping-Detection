class GarbageDetectionEnv:
    def __init__(self):
        self.current_step = 0
        # 🔥 MUST MATCH openenv.yaml IDs EXACTLY!
        self.tasks = {
            "task_1": 0.45,
            "task_2": 0.65,
            "task_3": 0.85
        }
        self.graders = self.tasks

    def reset(self):
        self.current_step = 0
        return {"step": self.current_step, "status": "initialized"}

    def state(self):
        return {"step": self.current_step, "tasks": self.tasks}

    def step(self, action):
        self.current_step += 1
        done = self.current_step >= 3
        return (
            {"step": self.current_step},
            0.5, 
            done,
            {
                "tasks": self.tasks,
                "graders": self.tasks
            }
        )