#!/usr/bin/env python3

import argparse
from random import randint

import matplotlib.pyplot as plot
from collections import Counter
import numpy as np

def run_simulations(num, simulations, kata, rerolls):
	results = []

	for i in range(simulations):
		results.append(run_simulation(num, kata, rerolls))

	hist = Counter(results)
	
	keys = hist.keys()
	vals = hist.values()

	plot.bar(keys, np.divide(list(vals), simulations))
	plot.show()


def run_opposed(attack, defence, simulations, kata, rerolls, defender_kata, defender_rerolls):
	results = []

	for i in range(simulations):
		results.append(run_simulation(attack, kata, rerolls) - run_simulation(defence, defender_kata, defender_rerolls))

	hist = Counter(results)
	
	keys = hist.keys()
	vals = hist.values()

	plot.bar(keys, np.divide(list(vals), simulations))
	plot.show()

def run_simulation(num, kata, rerolls):
	rolls = []
	for i in range(num):
		rolls.append(d6())

	rolls.sort()

	for i in range(min(rerolls, num)):
		if rolls[i] < 6:
			rolls[i] = d6()

	if not kata:
		rolls = [x for x in rolls if x > 1]

	if len(rolls) > 0:
		return max(rolls) + min(len(rolls) - 1, 2)

	return 0

def d6():
	return randint(1, 6)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simulates rolling bushido dice")
    parser.add_argument('-n', '--num', required=True, help="the number of dice to roll", type=int)
    parser.add_argument('-s', '--simulations', required=True, help="the numnber of simulations to run", type=int)
    parser.add_argument('-k', '--kata', default=False, help="does the model have Kata")
    parser.add_argument('-rr', '--rerolls', default=0, help='the number of rerolls', type=int)
    parser.add_argument('-d', '--defence', default=0, help='the number of dice to defend with, if included will run opposed simulations', type=int)
    parser.add_argument('-dk', '--d_kata', default=False, help="does the defender have Kata")
    parser.add_argument('-drr', '--d_rerolls', default=0, help='the number of rerolls for the defender', type=int)

    args = parser.parse_args()

    if args.defence == 0:
    	run_simulations(args.num, args.simulations, args.kata, args.rerolls)
    else:
    	run_opposed(args.num, args.defence, args.simulations, args.kata, args.rerolls, args.d_kata, args.d_rerolls)
