from tournament.models.tournament import Tournament
from tournament.services.sql_service import SQLService

import json

class TournamentManager():

    def __init__(self, sql_service):
        self.sql: SQLService = sql_service
        self.tournaments: dict[int, Tournament] = {}
        self._load()

    def _load(self):
        rows = self.sql.fetchall("SELECT id FROM tournaments")
        for row in rows:
            tournament_id = row["id"]
            tournament = Tournament(self.sql, tournament_id)
            if tournament.exists():
                self.tournaments[tournament_id] = tournament
            else:
                self.tournaments[tournament_id] = None

    def get_tournament(self, tournament_id: int):
        if tournament_id not in self.tournaments:
            tournament = Tournament(self.sql, tournament_id)
            if tournament.exists():
                self.tournaments[tournament_id] = tournament
            else:
                self.tournaments[tournament_id] = None
        return self.tournaments[tournament_id]
    
    def create_tournament(self, name: str = None, region: str = None, date: str = None,
                          team_size: int = None, state: str = None, has_bots: bool = False,
                          banned_characters: list[str] = [], banned_maps: list[str] = [],
                          rules: list[str] = [], prizes: list[str] = [], is_official: bool = False):

        tournament_id = self.sql.execute(
            """
            INSERT INTO tournaments (
                name, region, date, team_size, state, has_bots,
                banned_characters, banned_maps, rules, prizes, is_official
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                region,
                date,
                team_size,
                state,
                int(has_bots),
                json.dumps(banned_characters),
                json.dumps(banned_maps),
                json.dumps(rules),
                json.dumps(prizes),
                int(is_official)
            )
        )
        
        self.tournaments[tournament_id] = Tournament(self.sql, tournament_id)
        
    def delete_tournament(self, tournament_id: int):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            self.sql.execute("DELETE FROM tournaments WHERE id = ?", (tournament_id,))
            del self.tournaments[tournament_id]