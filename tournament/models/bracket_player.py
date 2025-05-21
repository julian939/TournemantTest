from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.tournament import Tournament

class BracketPlayer():

    def __init__(self, sql: SQLService, bracket_id: int, player_id):
        self.sql: SQLService = sql
        self.bracket_id: int = bracket_id
        self.player_id: int = player_id

        self.points: Optional[int] = None

        if self.exists():
            self._load()

    def _load(self):
        ... 

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM bracket_players WHERE bracket_id = ? AND player_id = ?",
            (self.bracket_id, self.player_id)
        )
        return row is not None