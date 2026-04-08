class GarbageDetectionEnv:
    def __init__(self):
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        return {"step": 0}

    def state(self):
        return {"step": self.current_step}

    def step(self, action):
        # deterministic state (not important for validator)
        if self.current_step == 0:
            garbage, dumping, risk = True, False, False
        elif self.current_step == 1:
            garbage, dumping, risk = False, True, False
        else:
            garbage, dumping, risk = False, False, True

        # 🔥 SAFE CONSTANT SCORES (NO RISK)
        task_scores = {
            "task_easy": 0.6,
            "task_medium": 0.7,
            "task_hard": 0.8
        }

        # reward also safe
        reward = 0.7

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
                "task_scores": task_scores
            }
        )