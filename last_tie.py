#! /usr/bin/env python

from last_four import *

def if_tie():
	score_rem = [0, 0]
	wickets_rem = [1, 1]
	over_total = [1, 1]
	scoring_prob_team1 = {"Kohli": [5, 10, 25, 10, 25, 1, 14, 10],
				"Sodhi": [5, 15, 15, 10, 20, 1, 19, 15]}
	scoring_prob_team2 = {"DeVilliers": [5, 10, 25, 10, 25, 1, 14, 10],
				"Amla": [10, 15, 15, 10, 20, 1, 14, 15]}
	batsmen_score_team1 = {"Kohli": [0, 0], "Sodhi": [0, 0]}
	batsmen_score_team2 = {"DeVilliers": [0, 0], "Amla": [0, 0]}
	run_arr = [0, 1, 2, 3, 4, 5, 6, 7]
	batsmen_rem_team1 = []
	batsmen_rem_team2 = []
	batsmen_arr_team1 = ["Kohli", "Sodhi"]
	batsmen_arr_team2 = ["DeVilliers", "Amla"]
	score_prob = [scoring_prob_team1, scoring_prob_team2]
	bats_score = [batsmen_score_team1, batsmen_score_team2]
	batsmen_arr = [batsmen_arr_team1, batsmen_arr_team2]
	batsmen_rem = [batsmen_rem_team1, batsmen_rem_team2]
	_batsmen_ind = [0, 1]
	for over in range(over_total[0]):
		score_rem[0] += over_sim_score(over, _batsmen_ind, batsmen_rem[0],
						 bats_score[0], score_prob[0], batsmen_arr[0], wickets_rem[0])
		if wickets_rem[0]:
			logging.info("End of over %d. Score: %d\n", 
				over, score_rem[0])
		else:
			pass
			#logging.info("Score: %d\n", score_rem[0])
	logging.info("Team batting first has scored %d runs. Target %d in %d overs\n",
		 score_rem[0], score_rem[0] + 1, over_total[1])

	score_rem[1] = score_rem[0] + 1
	for over in range(over_total[1]):
		res = over_sim_chase(over, _batsmen_ind, batsmen_rem[1], bats_score[1], score_prob[1],
				batsmen_arr[1], wickets_rem[1], score_rem[1])
	if res[1] > 1:
		logging.critical("Chasing team has lost the match by %d runs",
				res[1] - 1)	
	else:
		logging.critical("Chasing team has won the match")
	logging.info("Scores: Team 1")
	for key in bats_score[0]:
		logging.info("\t\t%s: \t\t\t%d runs (%d balls)",	
			key, bats_score[0][key][0], bats_score[0][key][1])
	logging.info("        Team 2 ")
	for key in bats_score[1]:
		logging.info("\t\t%s: \t\t\t%d runs (%d balls)",	
			key, bats_score[1][key][0], bats_score[1][key][1])

if __name__ == "__main__":
	if_tie()
