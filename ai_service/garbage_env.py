class GarbageDetectionEnv:
    def __init__(self):
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        return {"step": 0, "status": "reset_done"}

    def state(self):
        return {"step": self.current_step}

    def step(self, action):
        self.current_step += 1
        done = self.current_step >= 3
        
        # EXACT SCHEMA: Tasks strictly containing 'graders' inside them
        info = {
            "tasks": {
                "task_1": {
                    "name": "Classification",
                    "score": 0.55,
                    "graders": { "main_grader": 0.55 }
                },
                "task_2": {
                    "name": "BoundingBox",
                    "score": 0.65,
                    "graders": { "main_grader": 0.65 }
                },
                "task_3": {
                    "name": "Reporting",
                    "score": 0.85,
                    "graders": { "main_grader": 0.85 }
                }
            }
        }

        return (
            {"step": self.current_step},
            0.5,
            done,
            info
        )