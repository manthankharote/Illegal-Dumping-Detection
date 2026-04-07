from .detector import GarbageDetector

class GarbageDetectionEnv:
    def __init__(self):
        self.detector = GarbageDetector()
        self.current_step = 0
        self.current_state = {}

    def reset(self):
        self.current_step = 0

        # initialize full state (IMPORTANT)
        self.current_state = {
            "step": self.current_step,
            "garbage": False,
            "dumping": False,
            "risk": False
        }

        return self.current_state

    def state(self):
        return self.current_state

    def step(self, action):
        pred = self.detector.detect()

        garbage = bool(pred.get("garbage", False))
        dumping = bool(pred.get("dumping", False))
        risk = bool(pred.get("risk", False))

        # simulate variation
        if self.current_step == 2:
            garbage = False

        reward = 0.0
        if action == 1 and garbage:
            reward = 1.0
        elif action == 2 and dumping:
            reward = 1.0
        elif action == 1 and risk:
            reward = 0.5

        self.current_step += 1

        # update full state (IMPORTANT)
        self.current_state = {
            "step": self.current_step,
            "garbage": garbage,
            "dumping": dumping,
            "risk": risk
        }

        done = False  # IMPORTANT: don't end immediately

        return self.current_state, float(reward), done, {}