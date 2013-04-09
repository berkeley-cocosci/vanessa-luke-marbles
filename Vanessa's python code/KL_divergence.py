# THIS IS A LIBRARY OF FUNCTIONS

# DESCRIPTION
# calculates the KL divergence of:
# two discrete probability distributions
# two matrices, where each row is a discrete probability distribution

# NOTES
# KL divergence is always the divergence of a model probability distribution from a data probability distribution.
# KL divergence is not symmetrical, divergence of data from model doesn't equal divergence of model from data,
# so correctly specify which array is the data one and which is the model one.
# Result is the number of extra nats that it would take to encode your data array with a code based on your model array.
# the unit of measurement is nats because the calculation uses the natural log.
# Result is 0 nats when the arrays are identical, or exactly proportional (every element is multiplied by some constant).  
# Lower limit = 0.  Upper limit is unbounded.  
# Where the model has probability zero, the data must have probability zero.  An error will be raised if this isn't the case.
# ln(0) is computed as 0 - wikipedia says 0*ln(0) can be computed as 0.  Is this any different than doing ln(0)=0?

import numpy as np
import sys

################################################################################ 
# RUN THESE FUNCTIONS

# calculates KL divergence of model_matrix[i] from data_matrix[i] (paired rows) in nats
# then sums the KL divergences of all the row pairs
def KL_two_matrices(data_matrix, model_matrix):
	DKLs = []
	for row in range(len(data_matrix)):
		#print "row: " + str(row)
		DKLs.append(KL_two_arrays(data_matrix[row], model_matrix[row]))
	#print DKLs # print each KL divergence per row
	return np.sum(DKLs)

# calculates KL divergence of model_matrix[i] from data_matrix[i] (paired rows) in nats
def KL_two_arrays(data_array, model_array):
	
	if len(data_array) != len(model_array):
		print "CANNOT COMPUTE: data array and model array must be of equal length"
		sys.exit()
	# the float(str(x)) business below allows array sums that equal 1 up to 11 decimal points to pass as 1
	# ex: 1.000000000002 (11 zeros) passes as 1, but 1.00000000002 (10 zeros) doesn't
	# this is to allow float rounding errors on actual values of 1 to pass through
	if float(str(sum(data_array))) != 1 and float(str(sum(model_array))) != 1:
		print "CANNOT COMPUTE: \ndata array does not sum to one \nmodel array does not sum to one"
		sys.exit()
	if float(str(sum(data_array))) != 1:
		print "CANNOT COMPUTE: data array does not sum to one"
		sys.exit()
	if float(str(sum(model_array))) != 1:
		print "CANNOT COMPUTE: model array does not sum to one"
		sys.exit()
	
	running_sum = 0
	for element in range(len(data_array)):
		if model_array[element] == 0 and data_array[element] != 0:
			print "CANNOT COMPUTE: model had probability zero where data exists"
			sys.exit()
		# these elifs set P(i)*ln(P(i)/Q(i)) = 0 if P(i)/Q(i) = 0, to avoid computing ln(0)
		elif data_array[element] != 0 and model_array[element] == 0:
			running_sum = 0
		elif data_array[element] == 0 and model_array[element] == 0:
			running_sum = 0
		elif data_array[element] == 0 and model_array[element] != 0:
			running_sum = 0
		else: running_sum = running_sum + ( data_array[element] * np.log(data_array[element] / model_array[element]) )
	return running_sum

################################################################################