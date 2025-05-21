from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.match import Match
import tournament.models.enums as Enums

class Round():

    def __init__(self, sql: SQLService, id: int):
        self.sql: SQLService = sql
        self.id: int = id

        self.state = Optional[Enums.RoundState] = None

        self.matches: dict[int, Match] = {}
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