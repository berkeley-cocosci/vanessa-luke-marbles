# THIS IS A PROGRAM

# DESCRIPTION



from scipy.special import beta as bta
import numpy as np
import math
import matplotlib.pyplot as py

# my libraries
import KL_divergence
import loglikelihood
import model_matrix_maker as mmm
import data_matrix_maker as dmm
import marbles_data as md


################################################################################ 
### SPECIFY

model = "m"
# "s" = sampler, "m" = MAP, "b" = binomial/drift, "f" = Luke's MAP with filter model
fitting = "loglike"
# "loglike", "KLdiv"
data = "m1"
# "m1" = 1-item task, "m6" = 6-item task, "m1_normed", "m6_normed"
draws = 10

# don't change these values unless you wanna re-code the x-axis labelling
# start = 0.1, stop = 20, divisions = 200
# values for alpha
start = 0.1
stop = 20
divisions = 200
alpha_range = np.linspace(start,stop,divisions)
ar = alpha_range.tolist()

################################################################################ 
### PROGRAM LOOP


fit_per_alpha = []
eLLN_fit_per_alpha = []
for alpha in alpha_range:
	
	fit = 0
	
	if data == "m1":
		data_matrix = dmm.create_1M_marble1_counts_Qmatrix(md.M1_ins_blue_counts, md.M1_outs_blue_counts)
	if data == "m1_normed":
		data_matrix = dmm.normalize_matrix_rows(dmm.create_1M_marble1_counts_Qmatrix(md.M1_ins_blue_counts, md.M1_outs_blue_counts))
	if data == "m6":
		data_matrix = dmm.create_6M_marble1_counts_Qmatrix(md.M6_ins_marble1_counts, md.M6_outs_marble1_counts)
	if data == "m6_normed":
		data_matrix = dmm.normalize_matrix_rows(dmm.create_6M_marble1_counts_Qmatrix(md.M6_ins_marble1_counts, md.M6_outs_marble1_counts))

	if model == "s":
		model_matrix = mmm.create_sampler_Qmatrix(draws, alpha)
	if model == "m":
		model_matrix = mmm.create_MAP_Qmatrix(draws, alpha)
	if model == "b":
		model_matrix = mmm.create_binomial_Qmatrix(draws)
	
	if fitting == "loglike":
		fit = loglikelihood.LL_two_matrices(data_matrix, model_matrix) # IDENTICAL to AlphaFit_plotter2.py method
		#fit = loglikelihood.LLN_two_matrices(data_matrix, model_matrix)
		
		eLLN_fit = loglikelihood.eLLN_two_matrices(data_matrix, model_matrix)
		eLLN_fit_per_alpha.append(eLLN_fit)
		
		fit_per_alpha.append(eLLN_fit)
	if fitting == "KLdiv":
		KL_fit = KL_divergence.KL_two_matrices(data_matrix, model_matrix)
		fit_per_alpha.append(KL_fit)


################################################################################
### PLOT

# TO DO: if KL, show min(y)
x = fit_per_alpha

if fitting == "loglike":
	max_y = max(x) # !!! if there are multiple maximums, it returns the first one, i.e the lowest alpha one!
	max_eLLN = max(eLLN_fit_per_alpha)  
if fitting == "KLdiv":
	min_y = min(x)
	
	
if model == "s": mod = "sampler"
if model == "m": mod = "MAP"
if model == "b": mod = "drift"

if data == "m1": dat = "1-item task (counts)"
if data == "m1_normed": dat = "1-item task (rows normalized)"
if data == "m6": dat = "6-item task (counts)"
if data == "m6_normed": dat = "6-item task (rows normalized)"
	
py.plot(ar,x)
py.xticks([ar[19],ar[39],ar[59],ar[79],ar[99],ar[119],ar[139],ar[159],ar[179],ar[199]], rotation=0)

if fitting == "loglike":
	py.title(mod +", "+str(dat) +"\nbest-fit alpha ~ "+ str(alpha_range[x.index(max(x))]) +" accounts for " +str(max_y) +"% of the data")
if fitting == "KLdiv":
	py.title(mod +", "+str(dat) +"\nbest-fit alpha ~ "+ str(alpha_range[x.index(max(x))]) +" has KL divergence = " +str(min_y))
	
py.show()













