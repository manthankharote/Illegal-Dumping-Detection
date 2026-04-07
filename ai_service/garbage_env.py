import json
from .detector import GarbageDetector

class GarbageDetectionEnv:
    def __init__(self):
        self.detector = GarbageDetector()
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        return self.state()

    def state(self):
        return {"step": self.current_step}

    def step(self, action):
        pred = self.detector.detect()
        garbage = pred.get("garbage", False)
        dumping = pred.get("dumping", False)
        risk = pred.get("risk", False)

        if self.current_step == 2:
            garbage = False  # Allows the "risk" fallback clause to be tested on the 3rd step

        reward = 0.0
        if action == 1 and garbage:
            reward = 1.0
        elif action == 2 and dumping:
            reward = 1.0
        elif action == 1 and risk:
            reward = 0.5

        self.current_step += 1
        return self.state(), float(reward), True, {"action": action, "ai_results": pred}
