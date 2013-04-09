# THIS IS A LIBRARY OF FUNCTIONS

# DESCRIPTION
# turns observed transitions between states into a transition matrix (a list of lists)
#
# INPUT: a list of input states and a list of output states
#        where in_counts[i] and out_counts[i] is a transition
# OUTPUT: a matrix of the raw trasitions in 2 formats: counts or normalized rows

################################################################################ 
### RUN THESE FUNCTIONS

def create_1M_marble1_counts_Qmatrix(in_counts, out_counts):
	matrix = [[0]*(11) for i in range(11)]
	for i in range(len(in_counts)):
		matrix[in_counts[i]][out_counts[i]] = matrix[in_counts[i]][out_counts[i]] + 1
	return matrix

def create_6M_marble1_counts_Qmatrix(in_counts, out_counts):
	matrix = [[0]*(11) for i in range(11)]
	for i in range(len(in_counts)):
		matrix[in_counts[i]][out_counts[i]] = matrix[in_counts[i]][out_counts[i]] + 1
	return matrix

# gives a matrix for the minority marble counts only! bottom half of matrix are all zeros.
def create_6M_minoritymarble_counts_Qmatrix(out_counts):
	in_count = [0,1,2,3,4,5]
	matrix = [[0]*(11) for i in range(11)]
	for participant in range(len(out_counts)):
		for bag in range(len(out_counts[0])):
			matrix[in_count[bag]][out_counts[participant][bag]] = matrix[in_count[bag]][out_counts[participant][bag]] + 1
	return matrix
	
def normalize_matrix_rows(matrix):
	new_matrix = [[0]*(11) for i in range(11)]
	for row in range(len(matrix)):
		#print "sum(row) is " +str(sum(matrix[row]))
		for element in range(len(matrix[row])):
			new_matrix[row][element] = matrix[row][element]/float(sum(matrix[row]))
	return new_matrix
	
################################################################################