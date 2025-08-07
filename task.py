from datetime import datetime
from enum import Enum


TASKS_FILE = "/home/iago/repos/trask/tasks.json"


class TaskState(Enum):
    DONE = "done"
    PRE = "pre"
    PR = "pr"
    STARTED = "started"
    PENDING = "pending"
    HOLD = "hold"

    @classmethod
    def from_str(cls, state_str):
        try:
            return cls(state_str.lower())
        except ValueError:
            raise ValueError(
                f"Estado inválido. Opciones: {', '.join([s.value for s in cls])}"
            )


class Task:
    def __init__(
        self,
        description,
        state=TaskState.PENDING,
        last_modified=None,
        uid=-1,
        repeat=False,
    ):
        self.uid = uid
        self.description = description
        self.state = state
        self.last_modified = last_modified or datetime.now().isoformat()
        self.repeat = repeat

    def to_dict(self):
        return {
            "uid": self.uid,
            "description": self.description,
            "state": self.state.value,
            "last_modified": self.last_modified,
            "repeat": self.repeat,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            uid=data.get("uid", -1),
            description=data["description"],
            state=TaskState(data["state"]),
            last_modified=data["last_modified"],
            repeat=data.get("repeat", False),
        )

    def update_state(self, new_state: TaskState):
        self.state = new_state
        self.last_modified = datetime.now().isoformat()
