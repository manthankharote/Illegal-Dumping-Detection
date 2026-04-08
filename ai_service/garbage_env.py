class GarbageDetectionEnv:
    def __init__(self):
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        return {"step": 0}

    def state(self):
        return {"step": self.current_step}

    def step(self, action):
        # deterministic scenarios
        if self.current_step == 0:
            garbage, dumping, risk = True, False, False
        elif self.current_step == 1:
            garbage, dumping, risk = False, True, False
        else:
            garbage, dumping, risk = False, False, True

        # ✅ ALWAYS VALID SCORES (0 < x < 1)
        task_easy = 0.3
        task_medium = 0.4
        task_hard = 0.5

        if garbage and action == 1:
            task_easy = 0.9
        if dumping and action == 2:
            task_medium = 0.8
        if risk and action == 1:
            task_hard = 0.7

        # final reward (also safe)
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
                "task_scores": {
                    "task_easy": float(task_easy),
                    "task_medium": float(task_medium),
                    "task_hard": float(task_hard)
                }
            }
        )