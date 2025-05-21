from enum import Enum, auto
from typing import Optional
import logging
from database.manager.sqlmanager import SQL
from database.objects.match import Match

class BracketState(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()

class Bracket():

    def __init__(self, bracket_id: int):
        self.bracket_id = bracket_id
        self.state = Optional[BracketState] = None
        self.db = SQL()

    def get_matches(self):
        return [Match(1), Match(2), Match(3)]

    '''
        GAMESTATE PRICIPLE
    '''

    def get_state(self) -> Optional[BracketState]:
        return self.state
    
    def set_state(self, new_state: BracketState):
        try:
            self.db.execute(
                "UPDATE brackets SET state = ? WHERE bracket_id = ?",
                (new_state.name, self.bracket_id)
            )
            self.state = new_state
            logging.info(f"Bracket state updated to '{new_state.name}' for Bracket ID {self.bracket_id}")
        except Exception as e:
            logging.error(f"Error updating state: {e}")

    def change_state(self, new_state: BracketState):
        allowed_transitions = {
            BracketState.NOT_STARTED: [BracketState.IN_PROGRESS],
            BracketState.IN_PROGRESS: [BracketState.FINISHED],
            BracketState.FINISHED: []
        }
        if self.state is None or new_state in allowed_transitions.get(self.state, []):
            self.set_state(new_state)
        else:
            raise ValueError(f"Invalid state transition from {self.state} to {new_state}")
