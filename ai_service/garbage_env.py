from .tasks import task_easy, task_medium, task_hard


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
        # 🔥 Deterministic simulation (3 tasks)
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

        # Update state
        self.current_state = {
            "step": self.current_step,
            "garbage": garbage,
            "dumping": dumping,
            "risk": risk
        }

        # 🔥 TASK GRADERS
        easy_score = task_easy(self.current_state, action)
        medium_score = task_medium(self.current_state, action)
        hard_score = task_hard(self.current_state, action)

        # Final reward (strictly between 0 and 1)
        reward = (easy_score + medium_score + hard_score) / 3

        self.current_step += 1

        done = False

        return self.current_state, float(reward), done, {
    "task_scores": {
        "task_easy": easy_score,
        "task_medium": medium_score,
        "task_hard": hard_score
    }
}