from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.tournament_player import TournamentPlayer
import tournament.models.enums as Enums
import logging

class Match():

    def __init__(self, sql: SQLService, id: int):
        self.sql: SQLService = sql
        self.id: int = id

        self.state = Optional[Enums.MatchState] = None
        self.host = Optional[TournamentPlayer] = None
        self.code = Optional[str] = None

        self.players: list[TournamentPlayer] = []

        if self.exists():
            self._load()

    def _load(self):
        row = self.sql.fetchone("SELECT * FROM matches WHERE id = ?", (self.id,))

        self.state = Enums.MatchState(row["state"]) if row["state"] else None
        self.host = TournamentPlayer(row["host"]) if row["host"] else None
        self.code = row["code"] if row["code"] else None

        self._load_players()

    def _load_players(self):
        rows = self.sql.fetchall("SELECT player_id FROM match_players WHERE match_id = ?", (self.id,))
        self.players = [TournamentPlayer(self.sql, row["player_id"]) for row in rows]

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM matches WHERE id = ?",
            (self.id,)
        )
        return row is not None
    
    def set_host(self, host: TournamentPlayer):
        try:
            self.sql.execute(
                "UPDATE matches SET host = ? WHERE id = ?",
                (host.player_id, self.id)
            )
            self.host = host
        except Exception as e:
            logging.error(f"Failed to set match host: {e}")

    def set_code(self, code: str):
        try:
            self.sql.execute(
                "UPDATE matches SET code = ? WHERE id = ?",
                (code, self.id)
            )
            self.code = code
        except Exception as e:
            logging.error(f"Failed to set match code: {e}")

    def set_to_next_state(self):
        if self.state == None:
            self.set_state(Enums.MatchState.PENDING)
        elif self.state == Enums.MatchState.PENDING:
            self.set_state(Enums.MatchState.IN_PROGRESS)
        elif self.state == Enums.MatchState.IN_PROGRESS:
            self.set_state(Enums.MatchState.FINISHED)
    
    def set_state(self, new_state: Enums.MatchState):
        try:
            self.sql.execute(
                "UPDATE matches SET state = ? WHERE id = ?",
                (new_state, self.id)
            )
            self.state = new_state
        except Exception as e:
            logging.error(f"Failed to set match state: {e}")

