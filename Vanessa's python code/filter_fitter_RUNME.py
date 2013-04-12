import numpy as np

# my libraries
import loglikelihood
import model_matrix_maker as mmm
import data_matrix_maker as dmm
import marbles_data as md


################################################################################ 
### SPECIFY

data = "m6"
# "m1" = 1-item task, "m6" = 6-item task, "m1_normed", "m6_normed"
draws = 10

# values for alpha
# start = 0, stop = 10, divisions = 201
# real bestfit alpha lies + or - 0.05 from the returned bestfit alpha
alpha_start = 0
alpha_stop = 10
alpha_divisions = 201
alpha_range = np.linspace(alpha_start,alpha_stop,alpha_divisions)
ar = alpha_range.tolist()
del ar[0]

# values for rho
# start = 0, stop = 1, divisions = 101
# real bestfit alpha lies + or - 0.01 from the returned bestfit alpha
rho_start = 0
rho_stop = 1
rho_divisions = 101
rho_range = np.linspace(rho_start,rho_stop,rho_divisions)
rr = rho_range.tolist()
del rr[0]


################################################################################ 
### PROGRAM LOOP

all_fits = []

for alpha in ar:
#for alpha in range(1,2): # when you want to get best-fit rho for a particular alpha
	for rho in rr:
	
		fit = 0
		if data == "m1":
			data_matrix = dmm.create_1M_marble1_counts_Qmatrix(md.M1_ins_blue_counts, md.M1_outs_blue_counts)
		if data == "m1_normed":
			data_matrix = dmm.normalize_matrix_rows(dmm.create_1M_marble1_counts_Qmatrix(md.M1_ins_blue_counts, md.M1_outs_blue_counts))
		if data == "m6":
			data_matrix = dmm.create_6M_marble1_counts_Qmatrix(md.M6_ins_marble1_counts, md.M6_outs_marble1_counts)
		if data == "m6_normed":
			data_matrix = dmm.normalize_matrix_rows(dmm.create_6M_marble1_counts_Qmatrix(md.M6_ins_marble1_counts, md.M6_outs_marble1_counts))
			
		model_matrix = mmm.create_MAP_filter_Qmatrix(draws, alpha, rho)
		fit = loglikelihood.eLLN_two_matrices(data_matrix, model_matrix)
		all_fits.append(fit)
			
################################################################################
### PLOT

bestfit_index = all_fits.index(max(all_fits))

bestfit_alpha = ar[bestfit_index/len(rr)] # next rho every alpha_divisions
bestfit_rho = rr[bestfit_index-((bestfit_index/len(rr))*len(rr))]

#bestfit_alpha = ar[bestfit_index/len(ar)] # next alpha every alpha_divisions
#bestfit_rho = rr[bestfit_index-((bestfit_index/len(ar))*len(ar))]

print "bestfit alpha ~ " +str(bestfit_alpha)
print "bestfit rho ~ " +str(bestfit_rho)

			
			
			
			
			
			
			
			
			
			
			
			
			
			
			