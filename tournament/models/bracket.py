from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.round import Round
import tournament.models.enums as Enums
import logging

class Bracket():

    def __init__(self, sql: SQLService, id: int):
        self.sql: SQLService = sql
        self.id: int = id

        self.state: Optional[Enums.BracketState] = None

        self.rounds: dict[int, Round] = {}
        self._load()

    def _load(self):
        row = self.sql.fetchone("SELECT * FROM brackets WHERE id = ?", (self.id,))

        self.state = Enums.BracketState(row["state"]) if row["state"] else None

        self._load_rounds()

    def _load_rounds(self):
        rows = self.sql.fetchall("SELECT round_id FROM bracket_rounds WHERE bracket_id = ?", (self.id,))
        for row in rows:
            self.get_round(row["round_id"])

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM brackets WHERE id = ?",
            (self.id,)
        )
        return row is not None
    
    def get_round(self, round_id: int) -> Round:
        if round_id not in self.rounds:
            round = Round(self.sql, round_id)
            if round.exists():
                self.rounds[round_id] = round
            else:
                self.rounds[round_id] = None
        return self.rounds[round_id]
    
    def get_state(self) -> Enums.BracketState:
        return self.state

    def set_to_next_state(self):
        if self.state == None:
            self.set_state(Enums.BracketState.PENDING)
        elif self.state == Enums.BracketState.PENDING:
            self.set_state(Enums.BracketState.IN_PROGRESS)
        elif self.state == Enums.BracketState.IN_PROGRESS:
            self.set_state(Enums.BracketState.FINISHED)
    
    def set_state(self, new_state: Enums.BracketState):
        try:
            self.sql.execute(
                "UPDATE brackets SET state = ? WHERE id = ?",
                (new_state, self.id)
            )
            self.state = new_state
        except Exception as e:
            logging.error(f"Failed to set bracket state: {e}")