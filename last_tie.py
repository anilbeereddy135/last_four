#! /usr/bin/env python

from last_four import *


if __name__ == "__main__":
	score_rem = 23
	wickets_rem = 1
	over_total = 1
	scoring_prob_team1 = {"Kohli": [5, 10, 25, 10, 25, 1, 14, 10],
				"Sodhi": [5, 15, 15, 10, 20, 1, 19, 15]}
	scoring_prob_team2 = {"DeVilliers": [5, 10, 25, 10, 25, 1, 14, 10],
				"Amla": [10, 15, 15, 10, 20, 1, 14, 15]}
	batsmen_score_team1 = {"Kohli": [0, 0], "Sodhi": [0, 0]}
	batsmen_score_team2 = {"DeVilliers": [0, 0], "Amla": [0, 0]}
	run_arr = [0, 1, 2, 3, 4, 5, 6, 7]

	score_prob = [scoring_prob_team1, scoring_prob_team2]
	bats_score = [batsmen_score_team1, batsmen_score_team2]

	
