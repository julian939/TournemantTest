import json
from typing import Optional
from datetime import datetime

from tournament.services.sql_service import SQLService
from tournament.models.bracket import Bracket
from tournament.models.tournament_player import TournamentPlayer
import tournament.models.enums as Enums
import logging

class Tournament():

    def __init__(self, sql: SQLService, id: int):
        self.sql: SQLService = sql
        self.id: int = id

        self.name: Optional[str] = None
        self.region: Optional[Enums.Region] = None
        self.date: Optional[datetime] = None
        self.team_size: Optional[int] = None
        self.state: Optional[Enums.TournamentState] = None
        self.has_bots: bool = False
        self.banned_characters: list[str] = [] 
        self.banned_maps: list[str] = []
        self.rules: list[str] = []
        self.prizes: list[str] = []
        self.is_official: bool = False

        self.brackets: dict[int, Bracket] = {}
        self.players: list[TournamentPlayer] = []
        
        if self.exists():
            self._load()

    def _load(self):
        row = self.sql.fetchone("SELECT * FROM tournaments WHERE id = ?", (self.id,))

        self.name = row["name"] if row["name"] else None
        self.region = Enums.Region(row["region"]) if row["region"] else None
        self.date = datetime.fromisoformat(row["date"]) if row["date"] else None
        self.team_size = row["group_size"] if row["group_size"] is not None else None
        self.state = Enums.TournamentState(row["state"]) if row["state"] else None
        self.has_bots = bool(row["has_bots"]) if row["has_bots"] is not None else False
            
        self.banned_characters = json.loads(row["banned_characters"]) if row["banned_characters"] else []
        self.banned_maps = json.loads(row["banned_maps"]) if row["banned_maps"] else []
        self.rules = json.loads(row["rules"]) if row["rules"] else []
        self.prizes = json.loads(row["prizes"]) if row["prizes"] else []
        self.is_official = bool(row["is_official"]) if row["is_official"] is not None else False

        self._load_brackets()
        self._load_players()

    def _load_brackets(self):
        rows = self.sql.fetchall("SELECT bracket_id FROM tournament_brackets WHERE tournament_id = ?", (self.id,))
        for row in rows:
            self.get_bracket(row["bracket_id"])

    def _load_players(self):
        rows = self.sql.fetchall("SELECT player_id FROM tournament_players WHERE tournament_id = ?", (self.id,))
        self.players = [TournamentPlayer(self.sql, row["player_id"]) for row in rows]

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM tournaments WHERE id = ?",
            (self.id,)
        )
        return row is not None

    def get_bracket(self, bracket_id: int) -> Bracket:
        if bracket_id not in self.brackets:
            bracket = Bracket(self.sql, bracket_id)
            if bracket.exists():
                self.brackets[bracket_id] = bracket
            else:
                self.brackets[bracket_id] = None
        return self.brackets[bracket_id]
    
    def add_bracket(self) -> Optional[int]:
        new_bracket_id = self.sql.execute(
            "INSERT INTO brackets (state) VALUES (?)",
            (Enums.BracketState.PENDING,)
        )
        if new_bracket_id:
            self.sql.execute(
                "INSERT INTO tournament_brackets (tournament_id, bracket_id) VALUES (?, ?)",
                (self.id, new_bracket_id)
            )  
            new_bracket = Bracket(self.sql, new_bracket_id)
            self.brackets[new_bracket_id] = new_bracket
            return new_bracket_id
        else:
            logging.error(f"Failed to create a new bracket for tournament {self.id}")
            return None
        
    def remove_bracket(self, bracket_id: int):
        if bracket_id in self.brackets:
            self.sql.execute(
                "DELETE FROM tournament_brackets WHERE tournament_id = ? AND bracket_id = ?",
                (self.id, bracket_id)
            )
            self.sql.execute(
                "DELETE FROM brackets WHERE id = ?",
                (bracket_id,)
            )
            del self.brackets[bracket_id]
        else:
            logging.warning(f"Bracket {bracket_id} does not exist in tournament {self.id}")

    