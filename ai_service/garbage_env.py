import numpy as np
import cv2
from detector import GarbageDetector

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
        """
        Advances the environment by one step.
        
        Args:
            action (int): 
                0 = ignore
                1 = detect garbage
                2 = alert
                
        Returns:
            next_state (dict): The state JSON after the action is taken.
            reward (float): The reward achieved perfectly bounded between 0.0 and 1.0.
            done (bool): Whether the episode has finished.
            info (dict): Additional diagnostic information including specific task score breakdown.
        """
        if self.current_step >= self.max_steps:
            return self.state(), 0.0, True, {"msg": "Episode finished"}
            
        info = {
            "action_taken": action,
            "tasks_evaluated": self.tasks,
        }
        
        # 1. Deterministic Call to AI Service (Garbage Detection Logic)
        ai_pred = self.detector.detect_frame(self.current_state)
        self.latest_ai_detections = ai_pred["detections"]
        info["ai_results"] = ai_pred
        
        # Ground truths for deterministic evaluation
        has_garbage = self.current_ground_truth.get("has_garbage", False)
        is_dumping = self.current_ground_truth.get("is_dumping", False)
        high_risk = self.current_ground_truth.get("high_risk", False)
        
        # 2. Reward Logic based on simulation of tasks (Easy -> Medium -> Hard)
        task_scores = {
            "garbage_detection": 0.0,
            "dumping_detection": 0.0,
            "risk_prediction": 0.0
        }

        # Task 1: Garbage Detection (Easy)
        # Target: Has garbage been accurately flagged?
        if has_garbage:
            task_scores["garbage_detection"] = 1.0 if action in [1, 2] else 0.0
        else:
            task_scores["garbage_detection"] = 1.0 if action == 0 else 0.0

        # Task 2: Dumping Detection (Medium)
        # Target: Has the system escalated appropriately for active dumping?
        if is_dumping:
            task_scores["dumping_detection"] = 1.0 if action == 2 else 0.0
        else:
            # If no dumping, action 2 is only justified if there is high risk
            task_scores["dumping_detection"] = 1.0 if (action != 2 or high_risk) else 0.0

        # Task 3: Risk Prediction (Hard)
        # Target: Has the system recognized high risk variables without explicitly needing dumping?
        if high_risk:
            task_scores["risk_prediction"] = 1.0 if action == 2 else 0.0
        else:
            # If no high risk, action 2 is only justified if there is active dumping
            task_scores["risk_prediction"] = 1.0 if (action != 2 or is_dumping) else 0.0

        # Overall deterministic reward perfectly scaled between 0.0 and 1.0
        reward = sum(task_scores.values()) / 3.0
        info["task_scores"] = task_scores

        # 3. Advance step counters
        self.current_step += 1
        done = self.current_step >= self.max_steps
        
        # 4. Grab state JSON *after* AI prediction to cleanly populate state
        next_state = self.state()
        
        # 5. Transition to the next scenario deterministically for the next iteration silently
        if not done:
            self._load_next_scenario()
            
        return next_state, reward, done, info
