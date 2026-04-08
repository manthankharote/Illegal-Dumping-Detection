class GarbageDetectionEnv:
    def __init__(self):
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        return {"step": 0}

    def state(self):
        return {"step": self.current_step}

    def step(self, action):
        # 🔥 Deterministic scenarios (3 tasks)
        if self.current_step == 0:
            garbage, dumping, risk = True, False, False
        elif self.current_step == 1:
            garbage, dumping, risk = False, True, False
        else:
            garbage, dumping, risk = False, False, True

        # ✅ Task scores (STRICTLY between 0 and 1)
        task_easy = 0.9 if garbage and action == 1 else 0.3
        task_medium = 0.8 if dumping and action == 2 else 0.4
        task_hard = 0.7 if risk and action == 1 else 0.5

        # Final reward
        reward = (task_easy + task_medium + task_hard) / 3

        self.current_step += 1

        return (
            {
                "step": self.current_step,
                "garbage": garbage,
                "dumping": dumping,
                "risk": risk
            },
            float(reward),
            False,
            {
                "tasks": [
                    {"name": "task_easy", "score": float(task_easy)},
                    {"name": "task_medium", "score": float(task_medium)},
                    {"name": "task_hard", "score": float(task_hard)}
                ]
            }
        )