from typing import Optional

from tournament.services.sql_service import SQLService

class Player():

    def __init__(self, sql: SQLService, id: int):
        self.sql: SQLService = sql
        self.id: int = id

        self.mmr: Optional[int] = None
        self._load()

    def _load(self):
        ...