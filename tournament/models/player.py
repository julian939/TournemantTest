from typing import Optional

from tournament.services.sql_service import SQLService

import logging

class Player():

    def __init__(self, sql: SQLService, id: int):
        self.sql: SQLService = sql
        self.id: int = id

        self.mmr: int = 0
        self._load()

    def _load(self):
        row = self.sql.fetchone("SELECT * FROM players WHERE id = ?", (self.id,))

        self.mmr = row["mmr"] if row["mmr"] is not None else 0

    def exists(self) -> bool:
        row = self.sql.fetchone(
            "SELECT * FROM players WHERE id = ?",
            (self.id,)
        )
        return row is not None
    
    def add_mmr(self, mmr: int):
        if mmr < 0:
            logging.error(f"MMR cannot be negative. Player {self.id} attempted to set MMR to {mmr}.")
            return
        
        self.mmr += mmr
        self.sql.execute(
            "UPDATE players SET mmr = ? WHERE id = ?",
            (self.mmr, self.id)
        )

    def remove_mmr(self, mmr: int):
        if mmr < 0:
            logging.error(f"MMR cannot be negative. Player {self.id} attempted to remove {mmr} MMR.")
            return
        
        if mmr > self.mmr:
            logging.error(f"Cannot remove {mmr} MMR from player {self.id} as it exceeds current MMR of {self.mmr}.")
            return
        
        self.mmr -= mmr
        self.sql.execute(
            "UPDATE players SET mmr = ? WHERE id = ?",
            (self.mmr, self.id)
        )

    def reset_mmr(self):
        self.remove_mmr(self.mmr)