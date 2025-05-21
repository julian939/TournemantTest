from enum import Enum, auto
from typing import Optional
import logging
from database.manager.sqlmanager import SQL

class MatchState(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()

class Match():

    def __init__(self, match_id: int):
        self.match_id = match_id
        self.state = Optional[MatchState] = None
        self.db = SQL()

    '''
        GAMESTATE PRICIPLE
    '''

    def get_state(self) -> Optional[MatchState]:
        return self.state
    
    def set_state(self, new_state: MatchState):
        try:
            self.db.execute(
                "UPDATE matchs SET state = ? WHERE match_id = ?",
                (new_state.name, self.match_id)
            )
            self.state = new_state
            logging.info(f"Match state updated to '{new_state.name}' for Match ID {self.match_id}")
        except Exception as e:
            logging.error(f"Error updating state: {e}")

    def change_state(self, new_state: MatchState):
        allowed_transitions = {
            MatchState.NOT_STARTED: [MatchState.IN_PROGRESS],
            MatchState.IN_PROGRESS: [MatchState.FINISHED],
            MatchState.FINISHED: []
        }
        if self.state is None or new_state in allowed_transitions.get(self.state, []):
            self.set_state(new_state)
        else:
            raise ValueError(f"Invalid state transition from {self.state} to {new_state}")
