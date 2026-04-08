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
        # 🔥 Deterministic simulation (NO detector)
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

        # Reward strictly between (0,1)
        reward = 0.2  # default

        if action == 1 and garbage:
            reward = 0.9
        elif action == 2 and dumping:
            reward = 0.8
        elif action == 1 and risk:
            reward = 0.5

        self.current_step += 1

        self.current_state = {
            "step": self.current_step,
            "garbage": garbage,
            "dumping": dumping,
            "risk": risk
        }

        done = False  # keep environment running

        return self.current_state, float(reward), done, {}