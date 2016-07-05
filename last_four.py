#! /usr/bin/env python2.7

import os
import sys
import random
import logging

logging.basicConfig(level=logging.DEBUG, format=" %(levelname)s - %(message)s")
logger = logging.getLogger()

handler = logging.FileHandler('res.log')
logger.addHandler(handler)

with open('res.log', 'w') as inp:
	pass

logger.info("Start of the match")

def scored_on_ball(_batsman):
	k = random.uniform(0, 1)
	run = 0
	for prob in range(len(scoring_prob[batsmen_arr[_batsman]])):
		run +=(scoring_prob[batsmen_arr[_batsman]][prob])/100.0 
		if run >= k:
			return prob

def over_sim(_over_num, _batsmen_ind):
	global score_rem
	global wickets_rem
	for ball in range(1, 7):
		run_on_ball = scored_on_ball(_batsmen_ind[0])
		batsmen_score[batsmen_arr[_batsmen_ind[0]]][1] += 1
		if run_on_ball == 7:
			wickets_rem -= 1
			logger.info("Over %d.%d: %s got out", _over_num, ball, 
						batsmen_arr[_batsmen_ind[0]])
			if wickets_rem:
				_batsmen_ind[0] = batsmen_rem.pop(0)
			else:
				if score_rem:
					logger.critical("All out. Batting team lost by %d runs in" 
					" %d overs and %d balls\n", score_rem, _over_num, ball)
				else:
					logger.critical("All out in %d overs and %d balls."
						"Excellent we've got a tie\n", _over_num, ball)
					
				return 0
		else:
			batsmen_score[batsmen_arr[_batsmen_ind[0]]][0] += run_on_ball
			score_rem -= run_on_ball
			if run_on_ball == 1:
				logger.info("Over %d.%d: %s scores %d run", _over_num, ball, 
						batsmen_arr[_batsmen_ind[0]], run_on_ball)
			else:
				logger.info("Over %d.%d: %s scores %d runs", _over_num, ball, 
						batsmen_arr[_batsmen_ind[0]], run_on_ball)
			if run_on_ball % 2:
				_batsmen_ind[0], _batsmen_ind[1] = _batsmen_ind[1], _batsmen_ind[0]
		if score_rem < 0:
			logger.critical("Batting team has won by %d wickets and %d balls"
			" remaining\n", wickets_rem, ((over_total - _over_num)*6 + (6 - ball)))
			return 1
	if _over_num == 3 and score_rem > 0:
		logger.critical("Batting team lost the game by %d runs\n", score_rem)
	if _over_num == 3 and score_rem == 0:
		logger.critical("Excellent! We've got a tie\n")
	return 2

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
			ret = over_sim(over, _batsmen_ind)
			if ret > 1:
				pass
			else:
				break
			_batsmen_ind[0], _batsmen_ind[1] = _batsmen_ind[1], _batsmen_ind[0]
		for key in batsmen_score:
			logger.info("%s: %d(%d balls)", key, batsmen_score[key][0],
							 batsmen_score[key][1])
		logger.info("End of the Match\n")
