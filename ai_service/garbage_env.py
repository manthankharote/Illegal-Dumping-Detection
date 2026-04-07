import numpy as np
import cv2
from .detector import GarbageDetector

class GarbageDetectionEnv:
    """
    OpenEnv-compatible Environment for Garbage Detection
    """
    def __init__(self, model_path="best.pt"):
        # Initialize the AI service
        self.detector = GarbageDetector(model_path=model_path)
        
        # The 3 specific tasks included in this environment
        self.tasks = [
            "Garbage detection",
            "Illegal dumping detection",
            "Risk prediction"
        ]
        
        self.current_step = 0
        self.max_steps = 100
        self.current_state = None
        
        # Internal tracking for ground truth (used for reward calculation)
        self.current_ground_truth = {}
        
    def reset(self):
        """
        Resets the environment to an initial state.
        Returns the initial state.
        """
        self.current_step = 0
        self._load_next_scenario()
        return self.state()
        
    def _load_next_scenario(self):
        """
        Helper method to load the next state (e.g., fetching a new frame from a camera or dataset).
        """
        # Placeholder: creating a mock blank image for the state
        # In a real scenario, this would be `cap.read()` or loading an image file.
        self.current_state = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Mock ground truth for calculating rewards
        # You can dynamically set these based on your dataset labels
        self.current_ground_truth = {
            "has_garbage": True,     # Relates to Task 1: Garbage detection
            "is_dumping": False,     # Relates to Task 2: Illegal dumping detection
            "high_risk": True        # Relates to Task 3: Risk prediction
        }

    def state(self):
        """
        Returns the current state formatted as JSON (dictionary) matching openenv specs.
        """
        import base64
        _, buffer = cv2.imencode('.jpg', self.current_state)
        img_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "image_base64": img_b64,
            "tasks_simulated": [
                {"id": "garbage_detection", "active": self.current_ground_truth["has_garbage"]},
                {"id": "dumping_detection", "active": self.current_ground_truth["is_dumping"]},
                {"id": "risk_prediction", "active": self.current_ground_truth["high_risk"]}
            ],
            "ground_truth": self.current_ground_truth,
            "ai_detections": getattr(self, "latest_ai_detections", [])
        }
        
    def step(self, action):
        if self.current_step >= self.max_steps:
            return self.state(), 0.0, True, {"msg": "Episode finished"}
            
        info = {
            "action_taken": action,
            "tasks_evaluated": self.tasks,
        }
        
        # simulated deterministic detection
        pred = self.detector.detect()
        garbage = pred["garbage"]
        dumping = pred["dumping"]
        risk = pred["risk"]
        
        # update state for info
        info["ai_results"] = pred
        
        reward = 0.0
        
        # simplified reward logic
        if action == 1 and garbage:
            reward = 1.0
        elif action == 2 and dumping:
            reward = 1.0
        elif action == 1 and risk:
            reward = 0.5
            
        # Overall deterministic reward
        self.current_step += 1
        done = self.current_step >= self.max_steps
        
        next_state = self.state()
        
        if not done:
            self._load_next_scenario()
            
        return next_state, reward, done, info
