from enum import Enum, auto
from typing import Optional
import logging
from database.manager.sqlmanager import SQL

class TournamentState(Enum):
    SETUP = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()
    CANCELED = auto()

class Tournament():

    def __init__(self, tournament_id: int):
        self.tournament_id = tournament_id
        self.state = Optional[TournamentState] = None
        self.db = SQL()


    '''
        GAMESTATE PRICIPLE
    '''

    def get_state(self) -> Optional[TournamentState]:
        return self.state
    
    def set_state(self, new_state: TournamentState):
        try:
            self.db.execute(
                "UPDATE tournaments SET state = ? WHERE tournament_id = ?",
                (new_state.name, self.tournament_id)
            )
            self.state = new_state
            logging.info(f"Tournament state updated to '{new_state.name}' for Tournament ID {self.tournament_id}")
        except Exception as e:
            logging.error(f"Error updating state: {e}")

    def change_state(self, new_state: TournamentState):
        allowed_transitions = {
            TournamentState.SETUP: [TournamentState.IN_PROGRESS, TournamentState.CANCELED],
            TournamentState.IN_PROGRESS: [TournamentState.FINISHED],
            TournamentState.FINISHED: [],
            TournamentState.CANCELED: []
        }
        if self.state is None or new_state in allowed_transitions.get(self.state, []):
            self.set_state(new_state)
        else:
            raise ValueError(f"Invalid state transition from {self.state} to {new_state}")
