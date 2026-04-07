class GarbageDetectionEnv:
    def __init__(self):
        self.current_step = 0
        self.current_state = {}

    def reset(self):
        self.current_step = 0
        self.current_state = {
            "step": 0,
            "garbage": False,
            "dumping": False,
            "risk": False
        }
        return self.current_state

    def state(self):
        return self.current_state

    def step(self, action):
        # PURE SIMULATION (NO detector call)
        if self.current_step == 0:
            garbage = True
            dumping = False
            risk = False
        elif self.current_step == 1:
            garbage = False
            dumping = True
            risk = False
        else:
            garbage = False
            dumping = False
            risk = True

        reward = 0.0
        if action == 1 and garbage:
            reward = 1.0
        elif action == 2 and dumping:
            reward = 1.0
        elif action == 1 and risk:
            reward = 0.5

        self.current_step += 1

        self.current_state = {
            "step": self.current_step,
            "garbage": garbage,
            "dumping": dumping,
            "risk": risk
        }

        return self.current_state, float(reward), False, {}