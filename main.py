from openenv import OpenEnv
from ai_service.garbage_env import GarbageDetectionEnv

env = GarbageDetectionEnv()

app = OpenEnv(env).app