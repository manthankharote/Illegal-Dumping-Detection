import json
from .detector import GarbageDetector

class GarbageDetectionEnv:
    def __init__(self):
        self.detector = GarbageDetector()
        self.current_step = 0
        self.max_steps = 3

    def reset(self):
        self.current_step = 0
        return self.state()

    def state(self):
        return {
            "step": self.current_step,
            "max_steps": self.max_steps
        }

    def step(self, action):
        if self.current_step >= self.max_steps:
            return self.state(), 0.0, True, {"msg": "Done"}

        pred = self.detector.detect()
        garbage = pred.get("garbage", False)
        dumping = pred.get("dumping", False)
        risk = pred.get("risk", False)

        reward = 0.0
        if action == 1 and garbage:
            reward = 1.0
        elif action == 2 and dumping:
            reward = 1.0
        elif action == 1 and risk:
            reward = 0.5
        else:
            reward = 0.0

        self.current_step += 1
        done = self.current_step >= self.max_steps
        
        info = {
            "action": action,
            "ai_results": pred
        }

        return self.state(), float(reward), done, info
