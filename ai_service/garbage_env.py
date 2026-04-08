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

        # 🔥 DIFFERENT TASKS PER STEP
        if self.current_step == 1:
            task_scores = {
                "task_easy": 0.4
            }
        elif self.current_step == 2:
            task_scores = {
                "task_medium": 0.6
            }
        elif self.current_step == 3:
            task_scores = {
                "task_hard": 0.8
            }
        else:
            task_scores = {
                "task_extra": 0.5
            }

        done = self.current_step >= 3

        return (
            {"step": self.current_step},
            0.5,
            done,
            {
                "task_scores": {
                    k: float(v) for k, v in task_scores.items()
                }
            }
        )