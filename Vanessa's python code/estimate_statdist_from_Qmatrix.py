# PROGRAM DESCRIPTION
# numerically estimate the stationary distribution of a Qmatrix
# Qmatrix format: list of lists, where entries are probabilities and each row sums to one
#                 top row = input state 0, left column = output state 0

import random
import matplotlib.pyplot as py
from itertools import groupby as g
import numpy as np

def statdist(loops,state,Qmatrix,plot_subtitle): 
	# enter a start state as variable "state", suggestion: middle row, middle column
	# loops suggestion: 1 million
	
	# returns a numerical estimate of a Qmatrix's stationary distribution
	# also plots the stationary distribution
	
	print "Running..."
	
	state_history = []
	stationary_distribution = [0]*len(Qmatrix)
	
	# generate one chain of n transitions through the Qmatrix, where n = number loops
	for i in range(loops):
		state = weighted_choice(Qmatrix[state])
		state_history.append(state)
	# tally up the number of times the chain visited each state
	for i in range(len(Qmatrix)): # for each state
		for j in range(len(state_history)): # for each transition recorded
			if state_history[j] == i:
				stationary_distribution[i] += 1 # tally visits for state i
	# normalize the stationary distribution (the tally of visits per state)
	for i in range(len(stationary_distribution)):
		stationary_distribution[i] = stationary_distribution[i]/float(loops)
	
	print "Q matrix :" + str(Qmatrix)
	print "stationary distribution: " +str(stationary_distribution)
	print "Done."
	
	plot_array(stationary_distribution,plot_subtitle)
	
def weighted_choice(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

def plot_array(stationary_distribution,subtitle):
	py.figure(figsize=(10,6))
	#py.xlim([0,1])
	py.plot(stationary_distribution, color='black', lw=3)
	#py.plot(m6_statdist, color='grey', lw=3)
	py.ylim([0,1])
	py.title("numerically estimated stationary distribution\n"+str(subtitle))
	py.xlabel('States')
	py.ylabel('Probability Mass')
	py.show()