from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.tournament_player import TournamentPlayer

class TournamentTeam():

    def __init__(self, sql: SQLService, id: int, tournament_id: int):
        self.sql: SQLService = sql
        self.id: int = id
        self.tournament_id: int = tournament_id

        self.players: list[TournamentPlayer] = []
        self._load()

    def _load(self):
        self._load_players()

    def _load_players(self):
        rows = self.sql.fetchall("SELECT player_id FROM team_players WHERE team_id = ?", (self.id,))
        self.players = [TournamentPlayer(self.sql, self.tournament_id, row["player_id"]) for row in rows]

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM tournament_teams WHERE id = ? AND tournament_id = ?",
            (self.id, self.tournament_id)
        )
        return row is not None