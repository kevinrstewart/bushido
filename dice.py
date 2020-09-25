#!/usr/bin/env python3

import argparse
from random import randint

import matplotlib.pyplot as plot
from collections import Counter
from collections import OrderedDict
import numpy as np
from textwrap import wrap

def run_simulations(num, simulations, kata, rerolls, percent, cumulative):
	results = []

	for i in range(simulations):
		results.append(run_simulation(num, kata, rerolls, 0))

	generate_chart(results, simulations, num, 0, rerolls, percent, cumulative, False)


def run_opposed(attack, defence, simulations, kata, rerolls, unblockable, defender_kata, defender_rerolls, percent, cumulative, damage, damageMod):
	results = []

	for i in range(simulations):
		results.append(max(0, run_simulation(attack, kata, rerolls, 0) - run_simulation(defence, defender_kata, defender_rerolls, unblockable)))

	if damage:
		damageResults = []
		for res in results:
			damageResults.append(roll_damage(res, damageMod))
		generate_chart(damageResults, simulations, attack, defence, rerolls, percent, cumulative, damage)
	else:
		generate_chart(results, simulations, attack, defence, rerolls, percent, cumulative, damage)

def run_simulation(num, kata, rerolls, unblockable):
	rolls = []
	for i in range(num):
		rolls.append(d6())

	rolls.sort()

	for i in range(min(rerolls, num)):
		if rolls[i] < 6:
			rolls[i] = d6()

	if not kata:
		rolls = [x for x in rolls if x > 1]

	if unblockable > 0 and len(rolls) > 0:
		for i in range(unblockable):
			rolls.remove(max(rolls))
		
	if len(rolls) > 0:
		return max(rolls) + min(len(rolls) - 1, 2)

	return 0

def d6():
	return randint(1, 6)
	
def roll_damage(sl, damageMod):
	rolls = []

	#This is my lazy implementation of Strong/Weak, didn't add a parameter for it
	rolls.append(d6())
	rolls.append(d6())
	#rolls.append(d6())
	#rolls.sort(reverse=True)
	rolls.sort()

	damRoll = rolls[0] + rolls[1] + damageMod
	
	damVal = sl
	if damRoll == 2:
		damVal -= 3
	elif damRoll == 3:
		damVal -= 2
	elif damRoll == 4 or damRoll == 5:
		damVal -= 1
	elif damRoll == 6 or damRoll == 7 or damRoll == 8:
		damVal += 0
	elif damRoll == 9 or damRoll == 10:
		damVal += 1
	elif damRoll == 11:
		damVal += 2
	elif damRoll == 12:
		damVal += 3

	return max(0, damVal)

def generate_chart(results, simulations, num, defence, rerolls, percent, cumulative, damage):
	hist = Counter(results)

	sortedHist = OrderedDict(sorted(hist.items(), key=lambda t: t[0], reverse=True))

	if(cumulative):
		total = 0
		for k in sortedHist.keys():
			if total != 0:
				sortedHist[k] = sortedHist[k] + total
			total = sortedHist[k]

	keys = sortedHist.keys()
	vals = sortedHist.values()
	
	x = keys
	y = np.divide(list(vals), simulations)

	if(percent):
		y = np.multiply(np.divide(list(vals), simulations), 100)		


	bars = plot.bar(x, height=y, width=.4)
	xlocs, xlabs = plot.xticks()

	xlocs=[i for i in x]
	xlabs=[i for i in x]

	plot.xlabel('Success Level')
	plot.ylabel('Chance')
	
	title = f"Rolling {args.num} dice against def {args.defence} rerolling {args.rerolls}"
	
	plot.title("\n".join(wrap(title, 60)))


	if(cumulative):
		plot.xlabel('AT LEAST This Success Level')
	if(damage):
		plot.xlabel('Damage')
	if(cumulative and damage):
		plot.xlabel('AT LEAST This Much Damage')

	plot.xticks(xlocs, xlabs)

	for bar in bars:
		yval = bar.get_height()
		plot.text(bar.get_x(), yval + .005, round(yval, 2))

	plot.show()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Simulates rolling bushido dice")
	parser.add_argument('-n', '--num', required=True, help="the number of dice to roll", type=int)
	parser.add_argument('-s', '--simulations', required=True, help="the numnber of simulations to run", type=int)
	parser.add_argument('-k', '--kata', default=False, help="does the model have Kata")
	parser.add_argument('-rr', '--rerolls', default=0, help='the number of rerolls', type=int)
	parser.add_argument('-d', '--defence', default=0, help='the number of dice to defend with, if included will run opposed simulations', type=int)
	parser.add_argument('-dk', '--d_kata', default=False, help="does the defender have Kata")
	parser.add_argument('-drr', '--d_rerolls', default=0, help='the number of rerolls for the defender', type=int)
	parser.add_argument('-u', '--unblockable', default=0, help='the amount of unblockable', type=int)
	parser.add_argument('-p', '--percent', default=0, help='display values as percentages on graph', action='store_true')
	parser.add_argument('-c', '--cumulative', default=0, help='show cumulative chance of getting SL+', action='store_true')
	parser.add_argument('-rd', '--damage', default=0, help='roll for expected damage', action='store_true')
	parser.add_argument('-dm', '--damageMod', default=0, help='modified to damage roll', type=int)
	args = parser.parse_args()
	if args.defence == 0:
		run_simulations(args.num, args.simulations, args.kata, args.rerolls, args.percent, args.cumulative)
	else:
		run_opposed(args.num, args.defence, args.simulations, args.kata, args.rerolls, args.unblockable, args.d_kata, args.d_rerolls, args.percent, args.cumulative, args.damage, args.damageMod)
