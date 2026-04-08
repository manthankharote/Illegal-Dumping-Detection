def task_easy(state, action):
    # garbage detection
    if state.get("garbage") and action == 1:
        return 0.9
    return 0.2


def task_medium(state, action):
    # dumping detection
    if state.get("dumping") and action == 2:
        return 0.8
    return 0.3


def task_hard(state, action):
    # risk prediction
    if state.get("risk") and action == 1:
        return 0.7
    return 0.4