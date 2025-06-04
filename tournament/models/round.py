from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.match import Match
import tournament.models.enums as Enums
import logging

class Round():

    def __init__(self, sql: SQLService, id: int):
        self.sql: SQLService = sql
        self.id: int = id

        self.state = Optional[Enums.RoundState] = None

        self.matches: dict[int, Match] = {}

        if self.exists():
            self._load()

    def _load(self):
        row = self.sql.fetchone("SELECT * FROM rounds WHERE id = ?", (self.id,))

        self.state = Enums.RoundState(row["state"]) if row["state"] else None

        self._load_matches()

    def _load_matches(self):
        rows = self.sql.fetchall("SELECT match_id FROM round_matches WHERE round_id = ?", (self.id,))
        for row in rows:
            self.get_match(row["round_id"])

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM runds WHERE id = ?",
            (self.id,)
        )
        return row is not None
    
    def get_match(self, match_id: int) -> Match:
        if match_id not in self.matches:
            match = Match(self.sql, match_id)
            if match.exists():
                self.matches[match_id] = match
            else:
                self.matches[match_id] = None
        return self.matches[match_id]
    
    def add_match(self) -> Optional[int]:
        new_match_id = self.sql.execute(
            "INSERT INTO matches (state) VALUES (?)",
            (Enums.MatchState.PENDING,)
        )
        if new_match_id:
            self.sql.execute(
                "INSERT INTO round_matches (round_id, match_id) VALUES (?, ?)",
                (self.id, new_match_id)
            )  
            new_match = Match(self.sql, new_match_id)
            self.matches[new_match_id] = new_match
            return new_match_id
        else:
            logging.error(f"Failed to create a new match for round {self.id}")
            return None
        
    def remove_match(self, match_id: int):
        if match_id in self.matches:
            self.sql.execute(
                "DELETE FROM round_matches WHERE round_id = ? AND match_id = ?",
                (self.id, match_id)
            )
            self.sql.execute(
                "DELETE FROM matches WHERE id = ?",
                (match_id,)
            )
            del self.matches[match_id]
        else:
            logging.warning(f"Match {match_id} does not exist in round {self.id}")

    def set_to_next_state(self):
        if self.state == None:
            self.set_state(Enums.RoundState.PENDING)
        elif self.state == Enums.RoundState.PENDING:
            self.set_state(Enums.RoundState.IN_PROGRESS)
        elif self.state == Enums.RoundState.IN_PROGRESS:
            self.set_state(Enums.RoundState.FINISHED)
    
    def set_state(self, new_state: Enums.RoundState):
        try:
            self.sql.execute(
                "UPDATE rounds SET state = ? WHERE id = ?",
                (new_state, self.id)
            )
            self.state = new_state
        except Exception as e:
            logging.error(f"Failed to set round state: {e}")