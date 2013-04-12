import numpy as np

# my libraries
import loglikelihood
import model_matrix_maker as mmm
import data_matrix_maker as dmm
import marbles_data as md


################################################################################ 
### SPECIFY

data = "m1"
# "m1" = 1-item task, "m6" = 6-item task, "m1_normed", "m6_normed"
draws = 10


################################################################################ 
### PROGRAM LOOP

zooms = 3

for zoom in range(zooms):

	if zoom == 0:
		# start = 0.1, stop = 20, divisions = 200
		# values for alpha
		alpha_start = 0
		alpha_stop = 20
		alpha_divisions = 21
		alpha_range = np.linspace(alpha_start,alpha_stop,alpha_divisions)
		ar = alpha_range.tolist()

		# start = 0.001, stop = 1, divisions = 200
		# values for rho
		rho_start = 0
		rho_stop = 1
		rho_divisions = 11
		rho_range = np.linspace(rho_start,rho_stop,rho_divisions)
		rr = rho_range.tolist()
	
	if zoom == 1:
		# values for alpha
		alpha_start = bestfit_alpha - 0.1
		alpha_stop = bestfit_alpha + 0.1
		alpha_divisions = 21
		alpha_range = np.linspace(alpha_start,alpha_stop,alpha_divisions)
		ar = alpha_range.tolist()

		# values for rho
		rho_start = bestfit_rho - 0.1
		rho_stop = bestfit_rho + 0.1
		rho_divisions = 11
		rho_range = np.linspace(rho_start,rho_stop,rho_divisions)
		rr = rho_range.tolist()
	
	if zoom == 2:
		# values for alpha
		alpha_start = bestfit_alpha - 0.01
		alpha_stop = bestfit_alpha + 0.01
		alpha_divisions = 51
		alpha_range = np.linspace(alpha_start,alpha_stop,alpha_divisions)
		ar = alpha_range.tolist()
		#  this iteration has +/- 0.0004 accuracy on either side of the bestfit alpha

		# values for rho
		rho_start = bestfit_rho - 0.02
		rho_stop = bestfit_rho + 0.02
		rho_divisions = 100
		rho_range = np.linspace(rho_start,rho_stop,rho_divisions)
		rr = rho_range.tolist()
		#  this iteration has +/- 0.0004 accuracy on either side of the bestfit rho


	all_fits = []

	for alpha in alpha_range:
		for rho in rho_range:
		
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
	### OUTPUT

	bestfit_index = all_fits.index(max(all_fits))

	bestfit_alpha = ar[bestfit_index/alpha_divisions]
	bestfit_rho = rr[bestfit_index-(alpha_divisions*(bestfit_index/alpha_divisions))]

	print "bestfit alpha ~ " +str(bestfit_alpha)
	print "bestfit rho ~ " +str(bestfit_rho)

			
			
			
			
			
			
			
			
			
			
			
			
			
			
			