from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.tournament_player import TournamentPlayer
import tournament.models.enums as Enums

class Match():

    def __init__(self, sql: SQLService, id: int):
        self.sql: SQLService = sql
        self.id: int = id

        self.state = Optional[Enums.MatchState] = None
        self.host = Optional[TournamentPlayer] = None
        self.code = Optional[str] = None

        self._load()

    def _load(self):
        row = self.sql.fetchone("SELECT * FROM matches WHERE id = ?", (self.id,))

        self.state = Enums.MatchState(row["state"]) if row["state"] else None
        self.host = TournamentPlayer(row["host"]) if row["host"] else None
        self.code = row["code"] if row["code"] else None

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM matches WHERE id = ?",
            (self.id,)
        )
        return row is not None

