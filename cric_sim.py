#! /usr/bin/env python2.7

import os
import sys
import random
import logging

#logging.basicConfig(filename='commentary.log', level=logging.DEBUG, format="%(message)s")
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
logger = logging.getLogger()

handler = logging.FileHandler('res.log')
logger.addHandler(handler)

with open('res.log', 'w') as inp:
	pass

logger.info("Start of the match\n")

def scored_on_ball(_batsman, _scoring_prob, _batsmen_arr):
	k = random.random()
	run = 0
	for prob in range(8):
		print 
		run += (_scoring_prob[_batsmen_arr[_batsman]][prob])/100.0
		if run >= k:
			return prob

def over_sim_chase(_over_num, _batsmen_ind, _batsmen_rem, _batsmen_score, _scoring_prob, _batsmen_arr, _wick, _score):
	for ball in range(1, 7):
		run_on_ball = scored_on_ball(_batsmen_ind[0], _scoring_prob, _batsmen_arr)
		_batsmen_score[_batsmen_arr[_batsmen_ind[0]]][1] += 1
		if run_on_ball == 7:
			_wick -= 1
			logger.info("Over %d.%d: %s got out", _over_num, ball, _batsmen_arr[_batsmen_ind[0]])
			if _wick:
				_batsmen_ind[0] = _batsmen_rem.pop(0)
			else:
				if _score - 1:
					logger.critical("All out. Chasing team lost by %d runs in" 
					" %d overs and %d balls\n", _score - 1, _over_num, ball)
				else:
					logger.critical("All out in %d overs and %d balls."
						" Excellent we've got a tie\n", _over_num, ball)
				return [_wick, _score, _batsmen_score]
		else:
			_batsmen_score[_batsmen_arr[_batsmen_ind[0]]][0] += run_on_ball
			_score -= run_on_ball
			if run_on_ball == 1:
				logger.info("Over %d.%d: %s scores %d run", 
					_over_num, ball, _batsmen_arr[_batsmen_ind[0]], run_on_ball)
			else:
				logger.info("Over %d.%d: %s scores %d runs", 
					_over_num, ball, _batsmen_arr[_batsmen_ind[0]], run_on_ball)
			if run_on_ball % 2:
				_batsmen_ind[0], _batsmen_ind[1] = _batsmen_ind[1], _batsmen_ind[0]
		if _score <= 0:
			logger.critical("Chasing team has won by %d wickets and %d balls"
			" remaining in %d over\n", _wick, (6 - ball), _over_num+1)
			return [_wick, _score, _batsmen_score]
	return [_wick, _score, _batsmen_score]


def over_sim_score(_over_num, _batsmen_ind, _batsmen_rem, _batsmen_score, _scoring_prob, _batsmen_arr, _wick):
	runs_scored = 0
	for ball in range(1, 7):
		run_on_ball = scored_on_ball(_batsmen_ind[0], _scoring_prob, _batsmen_arr)
		_batsmen_score[_batsmen_arr[_batsmen_ind[0]]][1] += 1
		if run_on_ball == 7:
			_wick -= 1
			logger.info("Over %d.%d: %s got out", _over_num, ball, _batsmen_arr[_batsmen_ind[0]])
			if _wick == 0:
				logger.critical("All out in %d.%d overs. Target is %d runs\n",
					 _over_num, ball, runs_scored)
				return [_wick, runs_scored, _batsmen_score]
			else:
				_batsmen_ind[0] = _batsmen_rem.pop(0)
		else:
			runs_scored += run_on_ball
			_batsmen_score[_batsmen_arr[_batsmen_ind[0]]][0] += run_on_ball
			if run_on_ball == 1:
				logger.info("Over %d.%d: %s scores %d run",
				 	_over_num, ball, _batsmen_arr[_batsmen_ind[0]], run_on_ball)
			else:
				logger.info("Over %d.%d: %s scores %d runs",
					 _over_num, ball, _batsmen_arr[_batsmen_ind[0]], run_on_ball)
			if run_on_ball % 2:
				_batsmen_ind[0], _batsmen_ind[1] = _batsmen_ind[1], _batsmen_ind[0]
	return [_wick, runs_scored, _batsmen_score]


def normal_sim():
	num_run = 1
	for i in range(num_run):
		over_total = 4
		score_rem = 40
		ball_rem = 24
		wickets_rem = 3
		batsmen_arr = ["Kohli", "Sodhi", "Ramurah", "Henra"]
		batsmen_rem = [2, 3]
		scoring_prob = {"Kohli": [5, 30, 25, 10, 15, 1, 9, 5], 
				"Sodhi": [10, 40, 20, 5, 10, 1, 4, 10],
				"Ramurah": [20, 30, 15, 5, 5, 1, 4, 20], 
				"Henra": [30, 25, 5, 0, 5, 1, 4, 30]}
		batsmen_score = {"Kohli": [0, 0], "Sodhi": [0, 0], 
				"Ramurah": [0, 0], "Henra": [0, 0]}
		run_arr = [0, 1, 2, 3, 4, 5, 6, 7]
		_batsmen_ind = [0, 1]
		for over in range(over_total):
			logging.info("%d overs left. %d runs to win. %d wickets remaining\n", 
					over_total - over, score_rem, wickets_rem)
			ret = over_sim_chase(over, _batsmen_ind, batsmen_rem, batsmen_score, scoring_prob,
						batsmen_arr, wickets_rem, score_rem)
			wickets_rem = ret[0]
			score_rem = ret[1]
			batsmen_score = ret[2]
			if ret[0] == 0 or ret[1] < 1:
				break
			else:
				pass
			_batsmen_ind[0], _batsmen_ind[1] = _batsmen_ind[1], _batsmen_ind[0]
		for key in batsmen_score:
			logger.info("%s: %d(%d balls)", key, batsmen_score[key][0], batsmen_score[key][1])
		logger.info("End of the Match\n")

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
		res = over_sim_score(over, _batsmen_ind, batsmen_rem[0],
				bats_score[0], score_prob[0], batsmen_arr[0], wickets_rem[0])
		wickets_rem[0] = res[0]
		score_rem[0] += res[1]
		bats_score[0] = res[2]
		if wickets_rem[0]:
			logging.info("End of over %d. Score: %d\n", over, score_rem[0])
		else:
			pass
                        #logging.info("Score: %d\n", score_rem[0])
	logging.info("Team batting first has scored %d runs. Target %d in %d overs\n",
		score_rem[0], score_rem[0] + 1, over_total[1])

	score_rem[1] = score_rem[0] + 1
	for over in range(over_total[1]):
		res = over_sim_chase(over, _batsmen_ind, batsmen_rem[1], bats_score[1], score_prob[1],
				batsmen_arr[1], wickets_rem[1], score_rem[1])
		wickets_rem[1] = res[0]
		score_rem[1] -= res[1]
		bats_score[1] = res[2]
		if wickets_rem[0]:
			logging.info("End of over %d. Score: %d\n", over, score_rem[1])
		else:   
			pass
                        #logging.info("Score: %d\n", score_rem[0])
	if res[1] > 1:
		logging.critical("Chasing team has lost the match by %d runs", res[1] - 1)
	else:
		logging.critical("Chasing team has won the match")
	logging.info("Scores: \nTeam 1\n")
	for key in bats_score[0]:
		logging.info("%s:\t %d runs (%d balls)", key, bats_score[0][key][0], bats_score[0][key][1])
	logging.info("\nTeam 2\n")
	for key in bats_score[1]:
		logging.info("%s:\t %d runs (%d balls)", key, bats_score[1][key][0], bats_score[1][key][1])


if __name__ == "__main__":
	normal_sim()
	if_tie()
