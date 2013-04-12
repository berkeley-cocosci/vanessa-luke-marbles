# PROGRAM

# DESCRIPTION
# this program calculates the loglikelihood and KL divergence (of 2 matrices) in parallel
# and makes their relationship explicit

import numpy as np
import KL_divergence 		# my library
import loglikelihood		# my library
import model_matrix_maker 	# my library
import alpha_fitter_RUNME as af	 # my library
import AlphaFit_plotter2 as af_old	# my library

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

def round_float(float,n_decimal_places):
	# note: this turns the float into string
	# good for comparing if two floats are the same up to a certain precision
	temp = '%.'+str(n_decimal_places)+'f'
	return temp % round(float,n_decimal_places)

def compare_list_of_floats(list1,list2,round_precision):
	boolean = "not set yet"
	rounded_list1 = []
	rounded_list2 = []
	if len(list1) == len(list2):
		for i in range(len(list1)):
			rounded_list1.append(round_float(list1[i],round_precision))
			rounded_list2.append(round_float(list2[i],round_precision))
		if rounded_list1 == rounded_list2:
			boolean = "same"
		else: boolen = "different"
	else: boolean = "lists aren't the same length"
	
	return boolean
		

################################################################################ 
# SCRATCH PAD

################################################################################
# equate KLdiv and LL

P = [0.8125, 0.0625, 0.0625, 0.0625] # data
Q = [0.5, 0.2, 0.2, 0.1] # model


# this is the relationship between KL divergence and log likelihood:
# a = b

a = KL_divergence.KL_two_arrays(P,Q)

b = -entropy_nats(P) - loglikelihood.LLN_two_arrays(P,Q)


################################################################################
# equate the alphafit results for different loglikelihood caluclation methods

