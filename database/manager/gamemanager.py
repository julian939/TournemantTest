import database.objects.tournament as tournament
import database.objects.bracket as bracket
import database.objects.match as match
import math

class GameManager():

    def __init__(self, tournament_id: int):
        self.tournament_id = tournament_id
        self.tournament = tournament.Tournament(self.tournament_id)
        self.brackets = self.tournament.get_brackets()
        

    def start_tournament(self):
        self.tournament.change_state(tournament.TournamentState.IN_PROGRESS)
        self.start_next_bracket()

    def start_next_bracket(self):
        bracket_state = bracket.BracketState
        for bracket_obj in self.brackets:
            if bracket_obj.get_state() == bracket_state.NOT_STARTED:
                bracket_obj.change_state(bracket_state.IN_PROGRESS)
                self.generate_matches_for_bracket(bracket_obj)
                break
        else:
            self.tournament.change_state(tournament.TournamentState.FINISHED)

    def is_bracket_finished(self, bracket: bracket.Bracket) -> bool:
        matches = bracket.get_matches()
        return all(match_obj.get_state() == match.MatchState.FINISHED for match_obj in matches)

    def generate_matches_for_bracket(self, bracket: bracket.Bracket):
        ...

    def _create_brackets(self, players: list[int], round):
        ...

    def _create_matches(self):
        ...

    def first_bracket_target(self, total_players: int) -> int:
        """
        Calculates the target number of players after the first bracket,
        so that the number is of the form 12 * 2^k.
        """
        if total_players <= 12:
            return total_players
        k = math.floor(math.log2(total_players / 12))
        return 12 * (2 ** k)

    def players_per_bracket(self, players_amount: int) -> list:
        """
        Returns a list of player counts:
        starting player count and the counts after each bracket,
        until 12 or fewer players remain.
        """
        if players_amount <= 12:
            return [players_amount]
        
        first_target = self.first_bracket_target(players_amount)
        results = [players_amount, first_target]
        
        current = first_target
        while current > 12:
            current = current // 2
            results.append(current)
        
        return results

    def brackets_amount(self, players_amount: int) -> int:
        """
        Returns the total number of brackets needed
        to reduce players_amount to 12 players.
        Counts the last bracket with the 12 players as well.
        """
        players_list = self.players_per_bracket(players_amount)
        brackets = len(players_list) - 1
        return max(brackets, 1)  # At least 1 bracket even if players <= 12

    def eliminations_in_first_bracket(self, players_amount: int) -> int:
        """
        Calculates how many players are eliminated in the first bracket
        to reach the target number for the first bracket.
        """
        target = self.first_bracket_target(players_amount)
        return players_amount - target