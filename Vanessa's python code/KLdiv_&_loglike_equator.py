# PROGRAM

# DESCRIPTION
# this program calculates the loglikelihood and KL divergence (of 2 matrices) in parallel
# and makes their relationship explicit

import numpy as np
import KL_divergence 		# my library
import loglikelihood		# my library
import model_matrix_maker 	# my library

def entropy_nats(discrete_probability_distribution):
	# can be an array of probabilities that sum to one, or counts that don't
	ent = 0
	total = sum(discrete_probability_distribution)
	for i in discrete_probability_distribution:
		p = i / float(total)
		if p == 0:
			ent += 0
		else: ent += p * np.log(p)
	return -ent



################################################################################ 
# SCRATCH PAD


P = [0.8125, 0.0625, 0.0625, 0.0625] # data
Q = [0.5, 0.2, 0.2, 0.1] # model


# this is the relationship between KL divergence and log likelihood:
# a = b

a = KL_divergence.KL_two_arrays(P,Q)

b = -entropy_nats(P) - loglikelihood.LLN_two_arrays(P,Q)