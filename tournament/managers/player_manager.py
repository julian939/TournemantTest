from tournament.models.player import Player
from tournament.services.sql_service import SQLService

class PlayerManager:
    
    def __init__(self, sql_service):
        self.sql: SQLService = sql_service
        self.players: dict[int, Player]
        self._load()

    def _load(self):
        rows = self.sql.fetchall("SELECT id FROM players")
        for row in rows:
            player_id = row["id"]
            player = Player(self.sql, player_id)
            if player.exists():
                self.players[player_id] = player
            else:
                self.players[player_id] = None

    def get_player(self, player_id: int):
        if player_id not in self.players:
            player = Player(self.sql, player_id)
            if player.exists():
                self.players[player_id] = player
            else:
                self.players[player_id] = None
        return self.players[player_id]

    def create_player(self):
        ...

    def delete_player(self, player_id: int):
        player = self.get_player(player_id)
        if player:
            self.sql.execute("DELETE FROM players WHERE id = ?", (player_id,))
            del self.players[player_id]
