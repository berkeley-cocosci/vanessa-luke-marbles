# THIS IS A LIBRARY OF FUNCTIONS

# DESCRIPTION

# data array must be in counts: times that the outcome was observed
# model array must be probabilities of each outcome
# both arrays must be of equal length

# LLN is equivalent for data arrays that are counts or probability dists that sum to 1

import numpy as np

################################################################################ 
# RUN THESE FUNCTIONS

def LL_two_arrays(data_array, model_array):
	running_sum = 0
	for i in range(len(data_array)):
		running_sum = running_sum + data_array[i]*(np.log(model_array[i]))
	return running_sum
	
def LLN_two_arrays(data_array, model_array):
	running_sum = 0
	for i in range(len(data_array)):
		running_sum = running_sum + data_array[i]*np.log(model_array[i])
	return running_sum/float(sum(data_array))

def eLLN_two_arrays(data_array, model_array):
	running_sum = 0
	for i in range(len(data_array)):
		running_sum = running_sum + data_array[i]*np.log(model_array[i])
	return np.e**(running_sum/float(sum(data_array)))


def LL_two_matrices(data_matrix,model_matrix):
	running_sum = 0
	for row in range(len(data_matrix)):
		running_sum = running_sum + LL_two_arrays(data_matrix[row], model_matrix[row])
	return running_sum

def LLN_two_matrices(data_matrix,model_matrix):
	running_sum = 0
	counts_sum = 0
	for row in range(len(data_matrix)):
		running_sum = running_sum + LL_two_arrays(data_matrix[row], model_matrix[row])
		counts_sum = counts_sum + sum(data_matrix[row])
	return running_sum/float(counts_sum)