# fantasy_baseball_simulation.py

import pandas as pd
import numpy as np
import random
import os
from sklearn.preprocessing import StandardScaler

# Constants
LINEUP_CONSTRAINTS = {
    "C": 2, "1B": 1, "2B": 1, "SS": 1, "3B": 1, "OF": 5,
    "CI": 1, "MI": 1, "UT": 1, "P": 9,
}
HITTER_CATEGORIES = ["HR", "RBI", "R", "SB", "AVG"]
PITCHER_CATEGORIES = ["W", "SV", "K", "ERA", "WHIP"]
NUM_WEEKS = 27
TEAM_COUNT = 15
ROUNDS = 50
NUM_SIMULATIONS = 10


class Player:
    def __init__(self, name, positions, stats):
        self.name = name
        self.positions = positions
        self.stats = stats
        self.weighted_value = 0
        self.standard_deviation = {}

    def calculate_weighted_value(self, z_scores, weights):
        self.weighted_value = sum(z_scores.get(cat, 0) * weights.get(cat, 1.0) for cat in z_scores.keys())

    def set_standard_deviation(self, variability_factor=0.1):
        self.standard_deviation = {stat: self.stats.get(stat, 0) * variability_factor for stat in self.stats.keys()}


class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        self.players = []

    def draft_player(self, player):
        self.players.append(player)

    def select_weekly_lineup(self, lineup_constraints):
        lineup = []
        remaining_slots = lineup_constraints.copy()
        sorted_players = sorted(self.players, key=lambda x: x.weighted_value, reverse=True)

        for player in sorted_players:
            for position in player.positions.split(","):
                if remaining_slots.get(position, 0) > 0:
                    lineup.append(player)
                    remaining_slots[position] -= 1
                    break

        return lineup
class League:
    """Manages the league and simulates drafts and games."""
    def __init__(self, teams, players):
        self.teams = teams
        self.players = players

    def simulate_snake_draft(self, rounds):
        if not self.players:
            raise ValueError("No players available for drafting.")
        draft_order = list(range(len(self.teams)))
        for round_num in range(rounds):
            current_order = draft_order if round_num % 2 == 0 else draft_order[::-1]
            for team_id in current_order:
                if self.players:
                    selected_player = self.players.pop(0)
                    self.teams[team_id].draft_player(selected_player)

    def evaluate_roto_standings(self, categories):
        """
        Evaluate roto standings based on category scores. For ERA and WHIP, lowest totals score highest points.
        """
        # Initialize a dictionary to store each team's total roto points
        roto_points = {team.team_id: 0 for team in self.teams}

        # Collect category totals for all teams
        category_totals = {cat: [] for cat in categories}
        for team in self.teams:
            for cat in categories:
                total = sum(player.stats.get(cat, 0) for player in team.players)
                category_totals[cat].append((team.team_id, total))

        # Rank teams and assign roto points for each category
        for cat, totals in category_totals.items():
            # Sort totals by category, special handling for ERA and WHIP
            if cat in ["ERA", "WHIP"]:
                sorted_totals = sorted(totals, key=lambda x: x[1])  # Ascending for ERA, WHIP
            else:
                sorted_totals = sorted(totals, key=lambda x: x[1], reverse=True)  # Descending for others

            # Assign roto points based on rankings
            for rank, (team_id, _) in enumerate(sorted_totals):
                roto_points[team_id] += TEAM_COUNT - rank

        # Convert roto points dictionary into sorted standings
        standings = sorted(roto_points.items(), key=lambda x: x[1], reverse=True)
        return standings


class Simulator:
    """Runs the fantasy baseball simulation."""
    def __init__(self, hitters_file, pitchers_file):
        self.hitters_file = hitters_file
        self.pitchers_file = pitchers_file
        self.players = []

    def load_projections(self):
        if not os.path.exists(self.hitters_file):
            raise FileNotFoundError(f"Hitters file not found: {self.hitters_file}")
        if not os.path.exists(self.pitchers_file):
            raise FileNotFoundError(f"Pitchers file not found: {self.pitchers_file}")

        hitters = pd.read_csv(self.hitters_file)
        pitchers = pd.read_csv(self.pitchers_file)

        required_categories = set(HITTER_CATEGORIES + PITCHER_CATEGORIES)
        if not required_categories.issubset(hitters.columns.union(pitchers.columns)):
            raise ValueError("Missing required categories in the projection files.")

        hitters["eligible_positions"] = hitters.get("YAHOO", "Unknown")
        pitchers["eligible_positions"] = "P"

        self.players = self._create_players(hitters, pitchers)

    def _create_players(self, hitters, pitchers):
        players = []
        for _, row in hitters.iterrows():
            players.append(Player(row["Name"], row["eligible_positions"], row.to_dict()))
        for _, row in pitchers.iterrows():
            players.append(Player(row["Name"], row["eligible_positions"], row.to_dict()))
        return players

    def compute_weighted_z_scores(self, weights):
        scaler = StandardScaler()
        for player in self.players:
            stats = {k: v for k, v in player.stats.items() if k in HITTER_CATEGORIES + PITCHER_CATEGORIES}
            z_scores = dict(zip(stats.keys(), scaler.fit_transform(pd.DataFrame([stats]))[0]))
            player.calculate_weighted_value(z_scores, weights)

    def evaluate_metrics(self, weights_list, num_simulations=NUM_SIMULATIONS):
        performance_metrics = {
            "average_position": [],
            "average_roto_score": [],
            "percent_first_place": [],
            "percent_top_three": [],
            "percent_below_10": [],
        }

        for weights in weights_list:
            print(f"Processing weight set: {weights}")
            test_team_positions = []
            test_team_scores = []
            first_place_count = 0
            top_three_count = 0
            below_10_count = 0

            for sim in range(num_simulations):
                # Create a fresh league with teams and players
                teams = [Team(team_id) for team_id in range(TEAM_COUNT)]
                league = League(teams, self.players[:])
                league.simulate_snake_draft(ROUNDS)

                # Assign a random test team
                test_team_id = random.choice(list(range(TEAM_COUNT)))

                # Calculate standings
                standings = league.evaluate_roto_standings(HITTER_CATEGORIES + PITCHER_CATEGORIES)
                test_team_position = next(
                    (pos for pos, (team_id, _) in enumerate(standings, start=1) if team_id == test_team_id), None)
                test_team_score = next((score for team_id, score in standings if team_id == test_team_id), 0)

                # Track results
                test_team_positions.append(test_team_position)
                test_team_scores.append(test_team_score)
                if test_team_position == 1:
                    first_place_count += 1
                if test_team_position <= 3:
                    top_three_count += 1
                if test_team_position > 10:
                    below_10_count += 1

            # Calculate metrics
            performance_metrics["average_position"].append(np.mean(test_team_positions))
            performance_metrics["average_roto_score"].append(np.mean(test_team_scores))
            performance_metrics["percent_first_place"].append(first_place_count / num_simulations)
            performance_metrics["percent_top_three"].append(top_three_count / num_simulations)
            performance_metrics["percent_below_10"].append(below_10_count / num_simulations)

        return performance_metrics


if __name__ == "__main__":
    simulator = Simulator("hitters_steamer_2024.csv", "pitchers_steamer_2024.csv")
    simulator.load_projections()

    weights_list = [
        {"HR": 1.5, "RBI": 1.2, "R": 1.0, "SB": 0.8, "AVG": 1.0, "W": 1.0, "SV": 1.0, "K": 1.0, "ERA": 0.8, "WHIP": 0.8},
        {"HR": 1.0, "RBI": 1.0, "R": 1.0, "SB": 1.5, "AVG": 1.0, "W": 1.0, "SV": 1.0, "K": 1.2, "ERA": 1.0, "WHIP": 1.0},
    ]

    simulator.compute_weighted_z_scores(weights_list[0])
    metrics = simulator.evaluate_metrics(weights_list)

    print("\nSimulation Metrics:")
    for i, weights in enumerate(weights_list):
        print(f"Weight Set {i + 1}: {weights}")
        print(f"  Average Position: {metrics['average_position'][i]:.2f}")
        print(f"  Average Roto Score: {metrics['average_roto_score'][i]:.2f}")
        print(f"  % First Place Finishes: {metrics['percent_first_place'][i]:.2%}")
        print(f"  % Top Three Finishes: {metrics['percent_top_three'][i]:.2%}")
        print(f"  % Below 10th Place: {metrics['percent_below_10'][i]:.2%}")
