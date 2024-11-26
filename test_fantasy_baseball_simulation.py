# test_fantasy_baseball_simulation.py

import unittest
from fantasy_baseball_simulation import Player, Team, League, Simulator

class TestPlayer(unittest.TestCase):
    def test_calculate_weighted_value(self):
        player = Player("Test Player", "1B", {"HR": 10, "RBI": 20})
        z_scores = {"HR": 1.5, "RBI": 2.0}
        weights = {"HR": 1.0, "RBI": 1.0}
        player.calculate_weighted_value(z_scores, weights)
        self.assertAlmostEqual(player.weighted_value, 3.5)

class TestTeam(unittest.TestCase):
    def test_draft_player(self):
        team = Team(1)
        player = Player("Test Player", "1B", {})
        team.draft_player(player)
        self.assertEqual(len(team.players), 1)

    def test_select_weekly_lineup(self):
        team = Team(1)
        player1 = Player("Player 1", "1B", {"HR": 10})
        player1.weighted_value = 50
        player2 = Player("Player 2", "1B", {"HR": 8})
        player2.weighted_value = 40
        team.draft_player(player1)
        team.draft_player(player2)
        lineup = team.select_weekly_lineup({"1B": 1})
        self.assertEqual(len(lineup), 1)
        self.assertEqual(lineup[0].name, "Player 1")

class TestLeague(unittest.TestCase):
    def test_simulate_snake_draft(self):
        teams = [Team(i) for i in range(3)]
        players = [Player(f"Player {i}", "1B", {}) for i in range(10)]
        league = League(teams, players)
        league.simulate_snake_draft(3)
        self.assertTrue(all(len(team.players) == 3 for team in teams))

    def test_evaluate_roto_standings(self):
        teams = [Team(i) for i in range(2)]
        player = Player("Player 1", "1B", {"HR": 10, "RBI": 20})
        teams[0].draft_player(player)
        league = League(teams, [])
        standings = league.evaluate_roto_standings(["HR", "RBI"])
        self.assertEqual(standings[0][0], 0)

class TestSimulator(unittest.TestCase):
    def test_load_projections_invalid_path(self):
        simulator = Simulator("invalid.csv", "invalid.csv")
        with self.assertRaises(FileNotFoundError):
            simulator.load_projections()

if __name__ == "__main__":
    unittest.main()
