import unittest

# =================================================================
# Section 1: The Main Class
# DO NOT modify this section.
# =================================================================
class TeamScores:
    def __init__(self):
        self.scores = {}

    def add_score(self, team_id: str, score: int):
        if not isinstance(score, int):
            raise ValueError("Score must be an integer")
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")
        if team_id not in self.scores:
            self.scores[team_id] = []
        self.scores[team_id].append(score)

    def average(self, team_id: str):
        if team_id not in self.scores or not self.scores[team_id]:
            raise ValueError("Team has no scores")
        return sum(self.scores[team_id]) / len(self.scores[team_id])

    def top_team(self):
        if not self.scores:
            raise ValueError("No teams available")
        averages = {team: self.average(team) for team in self.scores if self.scores[team]}
        if not averages:
            raise ValueError("No teams with scores available")
        max_avg = max(averages.values())
        return sorted([team for team, avg in averages.items() if avg == max_avg])

    def reset(self):
        self.scores.clear()


# =================================================================
# Section 2: The Unit Tests
# Students MUST complete this class.
# =================================================================
class TestTeamScores(unittest.TestCase):

    def setUp(self):
        """This method is called before each test function."""
        self.ts = TeamScores()
        # You can add some initial data here to use in your tests
        self.ts.add_score('team_A', 80)
        self.ts.add_score('team_B', 90)

    def test_add_score_valid(self):
        """
        Test adding a single valid score to a team.
        You should add a score and then check if it was correctly added.
        """
        
        self.ts.add_score('team_C', 95)
        self.assertEqual(self.ts.scores['team_C'], [95])

    def test_add_score_invalid_type(self):
        """
        Test that add_score raises a ValueError for non-integer scores.
        You should use a construct like: with self.assertRaises(ValueError):
        """
        with self.assertRaises(ValueError):
            self.ts.add_score('team_X', '90')
        with self.assertRaises(ValueError):
            self.ts.add_score('team_Y', 85.5)

    def test_add_score_invalid_range(self):
        """
        Test that add_score raises a ValueError for scores outside the 0-100 range.
        Check for both a score below 0 and a score above 100.
        """
        with self.assertRaises(ValueError):
            self.ts.add_score('team_X', -5)
        with self.assertRaises(ValueError):
            self.ts.add_score('team_Y', 150)

    def test_average(self):
        """
        Test that the average score for a team is calculated correctly.
        """
        self.ts.add_score('team_A', 100)
        avg = self.ts.average('team_A')
        self.assertEqual(avg, (80 + 100) / 2)

    def test_average_no_scores(self):
        """
        Test that average() raises a ValueError if a team has no scores.
        """
        self.ts.scores['team_empty'] = []
        with self.assertRaises(ValueError):
            self.ts.average('team_empty')

    def test_top_team(self):
        """
        Test that top_team() returns the team with the highest average score.
        """
        self.ts.add_score('team_A', 70)   
        self.ts.add_score('team_B', 95)   
        self.assertEqual(self.ts.top_team(), ['team_B'])
        
    def test_top_team_multiple_winners(self):
        """
        Test that top_team() returns a sorted list of team names if there is a tie.
        """
        self.ts.add_score('team_A', 100)  
        self.ts.add_score('team_B', 80)   
        self.ts.add_score('team_C', 90)   
        result = self.ts.top_team()
        self.assertEqual(result, ['team_A', 'team_C'])

    def test_reset(self):
        """
        Test that the reset() method correctly clears all team scores.
        After calling reset, the scores dictionary should be empty.
        """
        self.ts.reset()
        self.assertEqual(self.ts.scores, {})

    def test_reset_and_reuse(self):
        """
        Test that after calling reset(), we can reuse the TeamScores object normally.
        Ensures that reset() truly clears data and doesn't break functionality.
        """
        self.ts.add_score('team_X', 100)
        self.ts.add_score('team_Y', 70)
        self.ts.add_score('team_Y', 90)

        self.assertEqual(self.ts.average('team_Y'), 80)

        self.ts.reset()
        self.assertEqual(self.ts.scores, {})

        self.ts.add_score('team_X', 50)
        self.ts.add_score('team_X', 100)

        self.assertEqual(self.ts.average('team_X'), 75)

        self.assertNotIn('team_Y', self.ts.scores)



# =================================================================
# Section 3: Test Runner
# This part runs the tests when the script is executed.
# =================================================================
if __name__ == "__main__":
    unittest.main()