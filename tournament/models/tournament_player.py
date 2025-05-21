from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.tournament_team import TournamentTeam
from tournament.models.bracket_player import BracketPlayer
from tournament.models.match_player import MatchPlayer

class TournamentPlayer():

    def __init__(self, sql: SQLService, tournament_id: int, player_id: int):
        self.sql: SQLService = sql
        self.tournament_id: int = tournament_id
        self.player_id: int = player_id

        self.points: Optional[int] = None
        self.team: Optional[TournamentTeam] = None

        self._bracket_players: dict[int, BracketPlayer] = {}
        self._match_players: dict[int, MatchPlayer] = {}

        if self.exists():
            self._load()

    def _load(self):
        row = self.sql.fetchone("SELECT * FROM tournament_players WHERE tournament_id = ? AND player_id = ?", (self.tournament_id, self.player_id))

        self.points = row["points"] if row["points"] else None
        self.team = TournamentTeam(self.sql, row["team_id"], self.tournament_id) if row["team_id"] else None

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM tournament_players WHERE tournament_id = ? AND player_id = ?",
            (self.tournament_id, self.player_id)
        )
        return row is not None
    
    def get_bracket_player(self, bracket_id: int) -> Optional[BracketPlayer]:
        if bracket_id not in self._bracket_players:
            bracket_player = BracketPlayer(self.sql, bracket_id, self.player_id)
            if bracket_player.exists():
                self._bracket_players[bracket_id] = bracket_player
            else:
                self._bracket_players[bracket_id] = None
        return self._bracket_players[bracket_id]
    
    def get_match_player(self, match_id: int) -> Optional[MatchPlayer]:
        if match_id not in self._match_players:
            match_player = MatchPlayer(self.sql, match_id, self.player_id)
            if match_player.exists():
                self._match_players[match_id] = match_player
            else:
                self._match_players[match_id] = None
        return self._match_players[match_id]