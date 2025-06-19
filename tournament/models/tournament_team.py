from typing import Optional

from tournament.services.sql_service import SQLService
from tournament.models.tournament_player import TournamentPlayer

import logging

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
    
    def add_player(self, player_id: int):
        if any(player.player_id == player_id for player in self.players):
            logging.error("Player is already in the team.")
        try:
            self.sql.execute(
                "INSERT INTO team_players (team_id, player_id) VALUES (?, ?)",
                (self.id, player_id)
            )
            self.players.append(TournamentPlayer(self.sql, self.tournament_id, player_id))
        except Exception as e:
            logging.error(f"Failed to add player to team: {e}")

    def remove_player(self, player_id: int):
        if not any(player.player_id == player_id for player in self.players):
            logging.error("Player is not in the team.")
            return
        try:
            self.sql.execute(
                "DELETE FROM team_players WHERE team_id = ? AND player_id = ?",
                (self.id, player_id)
            )
            self.players = [player for player in self.players if player.player_id != player_id]
        except Exception as e:
            logging.error(f"Failed to remove player from team: {e}")