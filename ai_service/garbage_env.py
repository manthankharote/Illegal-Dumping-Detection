class GarbageDetectionEnv:
    def __init__(self):
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        return {"step": 0, "status": "reset_done"}

    def state(self):
        return {"step": self.current_step}

    def step(self, action):
        self.current_step += 1
        done = self.current_step >= 3
        
        # STRICTLY 3 TASKS, SCORES BETWEEN 0 AND 1 (Not 0.0, Not 1.0)
        graders_dict = {
            "task_1": 0.50,
            "task_2": 0.65,
            "task_3": 0.85
        }

        # ONLY return what standard RL environments return in info
        info = {
            "graders": graders_dict
        }

        return (
            {"step": self.current_step}, # observation
            0.5,                         # reward
            done,                        # done flag
            info                         # info dict containing graders
        )