from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.tournament_team import TournamentTeam
from tournament.models.bracket_player import BracketPlayer
from tournament.models.match_player import MatchPlayer

import logging

class TournamentPlayer():

    def __init__(self, sql: SQLService, tournament_id: int, player_id: int):
        self.sql: SQLService = sql
        self.tournament_id: int = tournament_id
        self.player_id: int = player_id

        self.points: int = 0
        self.team: Optional[TournamentTeam] = None

        self._bracket_players: dict[int, BracketPlayer] = {}
        self._match_players: dict[int, MatchPlayer] = {}

        if self.exists():
            self._load()

    def _load(self):
        row = self.sql.fetchone("SELECT * FROM tournament_players WHERE tournament_id = ? AND player_id = ?", (self.tournament_id, self.player_id))

        self.points = row["points"] if row["points"] else 0
        self.team = TournamentTeam(self.sql, row["team_id"], self.tournament_id) if row["team_id"] else None

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM tournament_players WHERE tournament_id = ? AND player_id = ?",
            (self.tournament_id, self.player_id)
        )
        return row is not None
    
    def set_team(self, team_id: int):
        new_team = TournamentTeam(self.sql, team_id, self.tournament_id)
        if not new_team.exists():
            logging.error(f"Team {team_id} does not exist.")
            return

        if self.team.id == team_id:
            logging.info(f"Player {self.player_id} is already in team {team_id}.")
            return
        
        new_team.add_player(self.player_id)
        self.team = new_team

    def add_points(self, points: int):
        if points < 0:
            logging.error("Cannot add negative points.")
            return

        self.points += points
        self.sql.execute(
            "UPDATE tournament_players SET points = ? WHERE tournament_id = ? AND player_id = ?",
            (self.points, self.tournament_id, self.player_id)
        )

    def remove_points(self, points: int):
        if points < 0:
            logging.error("Cannot remove negative points.")
            return

        if points > self.points:
            logging.error("Cannot remove more points than the player has.")
            return

        self.points -= points
        self.sql.execute(
            "UPDATE tournament_players SET points = ? WHERE tournament_id = ? AND player_id = ?",
            (self.points, self.tournament_id, self.player_id)
        )

    def reset_points(self):
        self.remove_points(self.points if self.points is not None else 0)

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