# run with marbles_data.py
# this is supposed to be a more efficient version of AlphaFit_plotter.py
# this version includes the MAP model the binomial Qmatrix

# INPUTS FIRST !!!

# paste these commands for the graphs:
# plot_alphafit_population((0,1,2,3,4,5),M6_GC)
# plot_alphafit_population((5,5,5,5,5,5),M6_all5050)
# plot_alphafit_population((0,0,0,0,0,0),M6_allReg)

# plot_alphafit_population(M1_ins_blue_counts,M1_outs_blue_counts)
# plot_alphafit_population(M6_ins_marble1_counts,M6_outs_marble1_counts) # produces exact same fits as "plot_alphafit_population((0,1,2,3,4,5),M6_GC)" but with different rounding errors

# plot_alphafit_population(M1_c2_ins,M1_c2_outs)
# plot_alphafit_population(M1_c5_ins,M1_c5_outs)
# plot_alphafit_population(W1_c2_ins,W1_c2_outs)
# plot_alphafit_population(W1_c5_ins,W1_c5_outs)


from scipy.special import beta as bta
import numpy as np
import math
import matplotlib.pyplot as py

model = "m"
# "s" = sampler, "m" = MAP, "b" = binomial/drift

# don't change these values unless you wanna re-code the x-axis labelling
# start = 0.1, stop = 20, divisions = 200
start = 0.1
stop = 20
divisions = 200
alpha_range = np.linspace(start,stop,divisions)
ar = alpha_range.tolist()

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
	middle = (input_m0count/float(draws))**output_m0count
	right = (1- (input_m0count/float(draws)))**(draws-output_m0count)		
	return (left * float(middle) * float(right))

def alphafit_population(input_m0count,output_m0count):
	loglike_per_alpha = []
	for alpha in alpha_range:
		#print "alpha = " +str(alpha)
		
		loglike = 0
		
		if len(input_m0count) == len(output_m0count):
			#print "equal data lengths"
		# assume input and output are arrays, where input[0] is paired with output[0]
			for participant in range(len(input_m0count)):
				i = input_m0count[participant]
				o = output_m0count[participant]
				#print "participant: " + str(participant) + ", " +str(i) + " -> " +str(o)+ ", " +str((math.log(transition_probability_calculator_sampler(i,o,alpha,10))))
		
				if model == "s":
					loglike = loglike + (math.log(transition_probability_calculator_sampler(i,o,alpha,10)))
				if model == "m":
					loglike = loglike + (math.log(transition_probability_calculator_MAP(i,o,alpha,10)))
				if model == "b":
					if transition_probability_calculator_binomial(i,o,10) == 0:
						loglike = loglike + 0
					else:
						loglike = loglike + (math.log(transition_probability_calculator_binomial(i,o,10)))
		
		if len(input_m0count) != len(output_m0count):
			#print "not equal data lengths"
		# assume input is an array and output is a matrix
		# it's possible len(matrix) = len(array)! in that case, this data set will go to the code above and the analysis will be incorrect.
			for element in range(len(input_m0count)):
				#print "ELEMENT: " +str(element)
				for participant in range(len(output_m0count)):
					i = input_m0count[element]
					o = output_m0count[participant][element]
					#print "participant: " + str(participant) + ", " +str(i) + " -> " +str(o)+ ", " +str((math.log(transition_probability_calculator_sampler(i,o,alpha,10))))
				
					if model == "s":
						loglike = loglike + (math.log(transition_probability_calculator_sampler(i,o,alpha,10)))
					if model == "m":
						loglike = loglike + (math.log(transition_probability_calculator_MAP(i,o,alpha,10)))
					if model == "b":
						if transition_probability_calculator_binomial(i,o,10) == 0:
							loglike = loglike + 0
						else:
							loglike = loglike + (math.log(transition_probability_calculator_binomial(i,o,10)))
		
		loglike_per_alpha.append(loglike)
			
	return loglike_per_alpha
			
def p_fit(likelihood,n_observations):
	return math.e**(likelihood/n_observations)
	
def ps_fit(likelihood_array,n_observations):
	array = []
	for i in range(len(likelihood_array)):
		array.append(math.e**(likelihood_array[i]/n_observations))
	return array

def plot_alphafit_population(input_m0count,output_m0count):
	x = alphafit_population(input_m0count,output_m0count)
	#print x
	max_y = max(x)  # !!! if there are multiple maximums, it returns the first one, i.e the lowest alpha one!
			
	if len(input_m0count) == len(output_m0count): # single marbles
		percent_fit = math.e**(max_y/(len(output_m0count)))
	if len(input_m0count) != len(output_m0count): # multi marbles
		percent_fit = math.e**(max_y/((len(output_m0count))*(len(input_m0count))))
		
	py.plot(ar,x)
	py.xticks([ar[19],ar[39],ar[59],ar[79],ar[99],ar[119],ar[139],ar[159],ar[179],ar[199]], rotation=0)
	py.title("population alpha fit: best-fit alpha ~ " + str(alpha_range[x.index(max(x))]) +",\nlog likelihood = " +str(max_y) + ", percent fit = " +str(percent_fit))
	
	print "model: " +str(model)
	print "best-fit alpha = " + str(alpha_range[x.index(max(x))])
	print "log likelihood = " +str(max_y)
	print "percent fit = " +str(percent_fit)

	py.show()
	
	return x

def M1_and_M6_dataset_plotter(M1_ins_blue_counts,M1_outs_blue_counts,M6_GC):
	M1 = alphafit_population(M1_ins_blue_counts,M1_outs_blue_counts)
	M6 = alphafit_population((0,1,2,3,4,5),M6_GC)

	M1_p = ps_fit(M1,192)
	M6_p = ps_fit(M6,64*6)
	
	py.rc('xtick', labelsize=16)
	py.rc('ytick', labelsize=16)
	py.plot(ar,M1_p, lw="3", color="blue")
	py.plot(ar,M6_p, lw="3", color="grey")
	py.xticks([ar[19],ar[39],ar[59],ar[79],ar[99],ar[119],ar[139],ar[159],ar[179],ar[199]])
	
	py.show()

def c2_W1_and_M1_dataset_plotter(W1_c2_ins,W1_c2_outs,M1_c2_ins,M1_c2_outs):
	W1 = alphafit_population(W1_c2_ins,W1_c2_outs)
	M1 = alphafit_population(M1_c2_ins,M1_c2_outs)

	W1_p = ps_fit(W1,29)
	M1_p = ps_fit(M1,32)
	
	py.rc('xtick', labelsize=16)
	py.rc('ytick', labelsize=16)
	py.plot(ar,W1_p, lw="3", color="grey")
	py.plot(ar,M1_p, lw="3", color="blue")
	py.xticks([ar[19],ar[39],ar[59],ar[79],ar[99],ar[119],ar[139],ar[159],ar[179],ar[199]])
	
	py.show()

def c5_W1_and_M1_dataset_plotter(W1_c5_ins,W1_c5_outs,M1_c5_ins,M1_c5_outs):
	W1 = alphafit_population(W1_c5_ins,W1_c5_outs)
	M1 = alphafit_population(M1_c5_ins,M1_c5_outs)

	W1_p = ps_fit(W1,len(W1_c5_outs))
	M1_p = ps_fit(M1,len(M1_c5_outs))
	
	py.rc('xtick', labelsize=16)
	py.rc('ytick', labelsize=16)
	py.plot(ar,W1_p, lw="3", color="grey")
	py.plot(ar,M1_p, lw="3", color="blue")
	#py.xticks([ar[19],ar[39],ar[59],ar[79],ar[99],ar[119],ar[139],ar[159],ar[179],ar[199]])
	py.xticks([ar[20],ar[100],ar[199]])
	
	py.show()

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