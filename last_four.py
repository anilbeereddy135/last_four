#! /usr/bin/env python2.7

import os
import sys
import random
import logging

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
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
		run += (_scoring_prob[_batsmen_arr[_batsman]][prob])/100.0
		if run >= k:
			return prob

def over_sim_chase(_over_num, _batsmen_ind, _batsmen_rem, _batsmen_score, _scoring_prob, _batsmen_arr, _wick, _score):
	for ball in range(1, 7):
		run_on_ball = scored_on_ball(_batsmen_ind[0], _scoring_prob, _batsmen_arr)
		_batsmen_score[_batsmen_arr[_batsmen_ind[0]]][1] += 1
		if run_on_ball == 7:
			_wick -= 1
			logger.info("Over %d.%d: %s got out", _over_num, ball, 
						_batsmen_arr[_batsmen_ind[0]])
			if _wick:
				_batsmen_ind[0] = _batsmen_rem.pop(0)
			else:
				if _score - 1:
					logger.critical("All out. Chasing team lost by %d runs in" 
					" %d overs and %d balls\n", _score - 1, _over_num, ball)
				else:
					logger.critical("All out in %d overs and %d balls."
						"Excellent we've got a tie\n", _over_num, ball)
					
				return [_wick, _score, _batsmen_score]
		else:
			_batsmen_score[_batsmen_arr[_batsmen_ind[0]]][0] += run_on_ball
			_score -= run_on_ball
			if run_on_ball == 1:
				logger.info("Over %d.%d: %s scores %d run", _over_num, ball, 
						_batsmen_arr[_batsmen_ind[0]], run_on_ball)
			else:
				logger.info("Over %d.%d: %s scores %d runs", _over_num, ball, 
						_batsmen_arr[_batsmen_ind[0]], run_on_ball)
			if run_on_ball % 2:
				_batsmen_ind[0], _batsmen_ind[1] = _batsmen_ind[1], _batsmen_ind[0]
		if _score <= 0:
			logger.critical("Chasing team has won by %d wickets and %d balls"
			" remaining in %d over\n", _wick, (6 - ball), _over_num)
			return [_wick, _score, _batsmen_score]
	if _over_num == 3 and score_rem > 1:
		logger.critical("Chasing team lost the game by %d runs\n", _score - 1)
	if _over_num == 3 and score_rem == 1:
		logger.critical("Excellent! We've got a tie\n")
	return [_wick, _score, _batsmen_score]


def over_sim_score(_over_num, _batsmen_ind, _batsmen_rem, _batsmen_score, _scoring_prob, _batsmen_arr, _wick):
	runs_scored = 0
	for ball in range(1, 7):
		run_on_ball = scored_on_ball(_batsmen_ind[0], _scoring_prob, _batsmen_arr)
		_batsmen_score[_batsmen_arr[_batsmen_ind[0]]][1] += 1
		if run_on_ball == 7:
			_wick -= 1
			logger.info("Over %d.%d: %s got out", _over_num, ball, 
				_batsmen_arr[_batsmen_ind[0]])
			if _wick == 0:
				logger.critical("All out in %d.%d overs. Target is %d runs\n",
					 _over_num, ball, runs_scored)
				return runs_scored
			else:
				_batsmen_ind[0] = _batsmen_rem.pop(0)
		else:
			runs_scored += run_on_ball
			_batsmen_score[_batsmen_arr[_batsmen_ind[0]]][0] += run_on_ball
			if run_on_ball == 1:
				logger.info("Over %d.%d: %s scores %d run", _over_num, ball, 
						_batsmen_arr[_batsmen_ind[0]], run_on_ball)
			else:
				logger.info("Over %d.%d: %s scores %d runs", _over_num, ball, 
						_batsmen_arr[_batsmen_ind[0]], run_on_ball)
			if run_on_ball % 2:
				_batsmen_ind[0], _batsmen_ind[1] = _batsmen_ind[1], _batsmen_ind[0]
	return runs_scored

if __name__ == "__main__":
	for i in range(100):
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
			logger.info("%s: %d(%d balls)", key, batsmen_score[key][0],
							 batsmen_score[key][1])
		logger.info("End of the Match\n")
