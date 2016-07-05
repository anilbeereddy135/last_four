#! /usr/bin/env python2.7

import os
import sys
import random
import logging

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger()

handler = logging.FileHandler('res.log')
logger.addHandler(handler)

logger.info("Start")

def scored_on_ball(_batsman):
	k = random.uniform(0, 1)
	run = 0
	for prob in range(len(scoring_prob[batsmen_arr[_batsman]])):
		run +=(scoring_prob[batsmen_arr[_batsman]][prob])/100.0 
		print scoring_prob[batsmen_arr[_batsman]][prob]/100.0
		print prob
		if run >= k:
			return scoring_prob[batsmen_arr[_batsman]][prob]

def over_sim(_over_num, _batsmen_ind):
	global _on_strike
	global score_rem
	global wickets_rem
	balls_to_end = 6
	runs_in_over = 0
	for ball in range(1, balls_to_end+1):
		run_on_ball = scored_on_ball(_batsmen_ind[0])
		batsmen_score[batsmen_arr[_batsmen_ind[0]]][1] += 1
		if run_on_ball == 7:
			wickets_rem -= 1
			logger.info("Over %d.%d: %s got out", _over_num, ball, 
						batsmen_arr[_batsmen_ind[0]])
			if wickets_rem:
				_batsmen_ind[0] = batsmen_rem.pop(0)
			else:
				logger.critical("Game over, all out. Batting team lost by %d runs", 
							score_rem)
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
			logger.critical("Batting team has won by %d wickets and %d balls remaining", 
					wickets_rem, ((3 - _over_num)*6 + (6 - ball)))
			return 1
	if _over_num == 3 and score_rem > 0:
		logger.critical("Batting team lost the game by %d runs", score_rem)
	if _over_num == 3 and score_rem == 0:
		logger.critical("Excellent! We've got a tie")
	return 2

if __name__ == "__main__":
	scoring_prob = {"Kohli": [5, 30, 25, 10, 15, 1, 9, 5], "Sodhi": [10, 40, 20, 5, 10, 1, 4, 10],
				"Ramurah": [20, 30, 15, 5, 5, 1, 4, 20], "Henra": [30, 25, 5, 0, 5, 1, 4, 30]}
	batsmen_arr = ["Kohli", "Sodhi", "Ramurah", "Henra"]
	score_arr_bat = []
	prob_arr = [0, 0, 0, 0, 0, 0, 0, 0]
	run_len = 100
	for i in range(run_len):
		score_arr_bat.append(scored_on_ball(0))
	for i in range(8):
		for item in score_arr_bat:
			if item == 7:
				print "There is an out"
			if item == i:
				prob_arr[i] += 1.0/run_len
	print prob_arr
	sys.exit()
	for i in range(100):
		over_total = 4
		score_rem = 40
		ball_rem = 24
		wickets_rem = 3
		batsmen_arr = ["Kohli", "Sodhi", "Ramurah", "Henra"]
		batsmen_rem = [2, 3]
		scoring_prob = {"Kohli": [5, 30, 25, 10, 15, 1, 9, 5], "Sodhi": [10, 40, 20, 5, 10, 1, 4, 10],
				"Ramurah": [20, 30, 15, 5, 5, 1, 4, 20], "Henra": [30, 25, 5, 0, 5, 1, 4, 30]}
		batsmen_score = {"Kohli": [0, 0], "Sodhi": [0, 0], "Ramurah": [0, 0], "Henra": [0, 0]}
		run_arr = [0, 1, 2, 3, 4, 5, 6, 7]
		_batsmen_ind = [0, 1]
		for over in range(over_total):
			ret = over_sim(over, _batsmen_ind)
			if ret > 1:
				pass
			else:
				break
			_batsmen_ind[0], _batsmen_ind[1] = _batsmen_ind[1], _batsmen_ind[0]
		for key in batsmen_score:
			logger.info("%s: %d(%d balls)", key, batsmen_score[key][0], batsmen_score[key][1])
