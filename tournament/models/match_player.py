from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.tournament import Tournament

class MatchPlayer():

    def __init__(self, sql: SQLService, match_id: int, player_id: int):
        self.sql: SQLService = sql
        self.match_id: int = match_id
        self.player_id: int = player_id

        self.points: Optional[int] = None

        if self.exists():
            self._load()

    def _load(self):
        ... 

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM match_players WHERE match_id = ? AND player_id = ?",
            (self.match_id, self.player_id)
        )
        return row is not None