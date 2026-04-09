import enum


class GameStatus(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    finished = "finished"
