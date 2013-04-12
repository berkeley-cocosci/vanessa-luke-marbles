# THIS IS A LIBRARY OF FUNCTIONS

# DESCRIPTION
# this program prints the transition matrices for a Bayesian learner with a given alpha and n draws
# uses the equations from Reali & Griffiths 2009 p.321
# for sampler & MAP learners
# and makes Qmatrix for drift (an agent that randomly samples from its observations) for n draws
# matrix format: matrix[row] returns the distribution of outputs per input count = row

# USEFUL:  print_matrix_formatted_for_R(matrix)

from scipy.special import beta as bta

################################################################################ 
# RUN THESE FUNCTIONS

# create sampler Q-matrix for N draws and a particular alpha value:
# cycles through all possible input-output pairs (row = input count of m0, column = output count of m0)
def create_sampler_Qmatrix(draws, alpha):
	matrix = [[0]*(draws+1) for i in range(draws+1)]
	for row in range(draws+1):
		for column in range(draws+1):
			matrix[row][column] = transition_probability_calculator_sampler(row,column,alpha,draws)
	return matrix
	
def create_MAP_Qmatrix(draws, alpha):
	matrix = [[0]*(draws+1) for i in range(draws+1)]
	for row in range(draws+1):
		for column in range(draws+1):
			matrix[row][column] = transition_probability_calculator_MAP(row,column,alpha,draws)
	return matrix
	
def create_binomial_Qmatrix(draws):
	matrix = [[0]*(draws+1) for i in range(draws+1)]
	for row in range(draws+1):
		for column in range(draws+1):
			matrix[row][column] = transition_probability_calculator_binomial(row,column,draws)
	return matrix

# Luke's filter model re-coded
def create_MAP_filter_Qmatrix(draws, alpha, rho):
	matrix = [[0]*(draws+1) for i in range(draws+1)]
	for row in range(draws+1):
		for column in range(draws+1):
			matrix[row][column] = transition_probability_calculator_MAP_filter(row,column,alpha,rho,draws)
	return matrix

### FORMAT OUTPUT FOR R
def print_matrix_formatted_for_R(matrix):
# just for draws = 10
	print "matrix <- array(1:121, dim=c(11,11))"
	for row in range(len(matrix)):
		a = str(matrix[row])[1:-1]
		print "matrix["+str(row+1)+",] <-c(" + str(a)+ ")"


################################################################################ 
# SUPPORT FUNCTIONS

# calculates transition probability of one input-output pair, using equation from Reali & Griffiths 2009 p.321
def transition_probability_calculator_sampler(input_m0count,output_m0count,alpha,draws):
	left = binomial_coefficient(draws,output_m0count)
	top = bta(input_m0count+output_m0count+(float(alpha)/2.),2*draws-input_m0count-output_m0count+(float(alpha)/2.))
	bottom = bta(input_m0count+(float(alpha)/2.),draws-input_m0count+(float(alpha)/2.))
	return (left * (float(top)/float(bottom)))
	
def transition_probability_calculator_MAP(input_m0count,output_m0count,alpha,draws):
	theta_substitute = (input_m0count + (alpha/2.0)) / (draws + alpha)
	left = binomial_coefficient(draws,output_m0count)
	middle = theta_substitute**output_m0count
	right = (1- theta_substitute)**(draws-output_m0count)
	return (left * float(middle) * float(right))

def transition_probability_calculator_binomial(input_m0count,output_m0count,draws):
	left = binomial_coefficient(draws,output_m0count)
	middle = (input_m0count/10.0)**output_m0count
	right = (1- (input_m0count/10.0))**(draws-output_m0count)
	return (left * float(middle) * float(right))

def transition_probability_calculator_MAP_filter(input_m0count,output_m0count,alpha,rho,draws):
	theta_substitute = ((rho*input_m0count) + (alpha/2.0)) / ((rho*draws) + alpha)
	left = binomial_coefficient(draws,output_m0count)
	middle = theta_substitute**output_m0count
	right = (1- theta_substitute)**(draws-output_m0count)
	return (left * float(middle) * float(right))

_bc_table={}
def binomial_coefficient(N, K):
    if str([N,K]) in _bc_table:
        return _bc_table[str([N,K])]
    else:
        if K>N:
            return 0
        if K > N - K: 
            K = N - K
        c = 1
        for i in range(K):
            c = c * (N - i)
            c = c / (i + 1)
        _bc_table[str([N,K])]=c
        return c

def column(matrix, i):  # returns the column of a matrix
    return [row[i] for row in matrix]

################################################################################