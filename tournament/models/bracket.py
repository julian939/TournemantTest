from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.round import Round
import tournament.models.enums as Enums

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

    # TODO add players as tournament players

    def _load_players(self):
        rows = self.sql.fetchall("SELECT player_id FROM tournament_players WHERE tournament_id = ?", (self.id,))
        self.players = [TournamentPlayer(self.sql, row["player_id"]) for row in rows]

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