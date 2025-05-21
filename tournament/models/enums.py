from enum import Enum, auto

class TournamentState(Enum):
    PENDING = auto()
    SETUP = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()
    CANCELED = auto()

class BracketState(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()

class RoundState(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()

class MatchState(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()
    CANCELED = auto()

class Region(Enum):
    EU = "EU"
    USW = "USW"
    US = "US"
    SA = "SA"
    OCE = "OCE"