import numpy as np
import pandas as pd


def separate_bins_feature(feat_column,special_case = False):
	no_bins = 10

	if special_case:
		# -- Solves the two special cases --
		max_val = 7
		min_val = 0
		single_bin = 1

	else:
		# -- All other cases --
		feat_column = feat_column.flatten()
		two_std = 2*np.std(feat_column)
		avg_val = np.mean(feat_column)

		# -- Finding the Range --
		if (avg_val - two_std < 0):
			min_val = 0
		else:
			min_val = round((avg_val - two_std),0)
		max_val = round((avg_val + two_std),0)

		# -- Creating the Bins --
		single_bin = (max_val - min_val) // no_bins
		if (single_bin == 0):
			single_bin = 1
	
	centre = min_val + (single_bin // 2)
	floor = min_val
	ceil = min_val + single_bin

	ranges = []
	bins = np.zeros(10)
	new_col = np.zeros(feat_column.shape[0])
	new_col_vals = np.zeros(feat_column.shape[0])

	for i in range(no_bins):
		range_str = ""
		if (centre <= max_val):
			for val_i in range(feat_column.shape[0]):
					if (i == 0):
						range_str = "x < " + str(ceil)
						if (feat_column[val_i] < ceil):
							new_col[val_i] = i
							new_col_vals[val_i] = centre

					elif (i == no_bins-1) or ((centre + single_bin) > max_val):
						range_str = str(floor) + " < x"
						if (feat_column[val_i] >= floor):
							new_col[val_i] = i
							new_col_vals[val_i] = centre

					else:
						range_str = str(floor) +" < x < " + str(ceil)
						if ((ceil > feat_column[val_i]) and (feat_column[val_i] >= floor)):
							new_col[val_i] = i
							new_col_vals[val_i] = centre
			bins[i] = centre
			ranges.append(range_str)
		
		else:
			bins[i] = -1
			ranges.append("-1")


		floor += single_bin
		ceil += single_bin
		centre += single_bin

	return bins, new_col, new_col_vals, ranges

def divide_data_bins(data, special=[]):
    no_feat = data.shape[1]
    bins_centred = []
    X_pos_array = []
    in_vals = []
    
    for i in range(no_feat):
        # Handles special case
        bins, new_col, val = separate_bins_feature(data[:,i].flatten(),(i in special))[:3]
        
        in_vals.append(val)
        bins_centred.append(bins)
        X_pos_array.append(new_col)
        
    # Convert to numpy array
    in_vals = np.array(in_vals).transpose()
    bins_centred = np.array(bins_centred)
    X_pos_array = (np.array(X_pos_array)).transpose() 

    return bins_centred, X_pos_array, in_vals


def prepare_for_analysis(filename):
	data_array = pd.read_csv(filename,header=None).values

	# -- Removes the columns with all -9 values -- 
	row_no = 0 
	for row in data_array:
		for col_i in range(1,row.shape[0]):
			if (row[col_i] == -9):
				remove = True
			else:
				remove = False
				break

		if remove:
			data_array = np.delete(data_array, row_no, 0)

		else:
			row_no += 1

	return data_array


def get_change_samples(pre_proc_file,all_data_file,cols,height):
	# 0-4 General Data
	# 5-8 Anchor Cols
	# 9-12 Change Cols
	# 13-16 Col Heights

	pre_data = pd.read_csv(pre_proc_file).values
	all_data = pd.read_csv(all_data_file,header=None).values

	change_samples = []

	# Identify Changes
	for test in range(9,14):
		for s in range(pre_data.shape[0]):
			if (pre_data[s][test] == cols):
				if (pre_data[s][test+5] == height):
					change_samples.append(s)

	return change_samples

def get_anch_samples(pre_proc_file,all_data_file,anchs):
	# 0-4 General Data
	# 5-8 Anchor Cols
	# 9-12 Change Cols
	# 13-16 Col Heights

	pre_data = pd.read_csv(pre_proc_file).values
	all_data = pd.read_csv(all_data_file,header=None).values
	anch_samples = []

	# Identify Anchors
	for test in range(5,9):
		for s in range(pre_data.shape[0]):
			if (pre_data[s][test] == anchs):
				anch_samples.append(s)

	return anch_samples



def sample_transf(X):
	trans_dict = {}
	my_count = 0
	for sample in range(10459):
		if X[sample][0] != -9:
			trans_dict[str(sample)] = my_count
			my_count += 1
		else:
			trans_dict[str(sample)] = -9

	return trans_dict



def prep_for_D3_global(pre_proc_file,all_data_file,samples,bins_centred,positions,transform):

	names = ["External Risk Estimate","Months Since Oldest Trade Open","Months Since Last Trade Open"
		,"Average Months in File","Satisfactory Trades","Trades 60+ Ever","Trades 90+ Ever"
		,"% Trades Never Delq.","Months Since Last Delq.","Max Delq. Last 12M","Max Delq. Ever","Total Trades"
		,"Trades Open Last 12M","% Installment Trades", "Months Since Most Recent Inq","Inq Last 6 Months"
		,"Inq Last 6 Months exl. 7 days", "Revolving Burden","Installment Burden","Revolving Trades w/ Balance"
		,"Installment Trades w/ Balance","Bank Trades w/ High Utilization Ratio","% trades with balance"]
	pre_data = pd.read_csv(pre_proc_file).values
	all_data = pd.read_csv(all_data_file,header=None).values[:,1:]

	final_data = []
	single_dict_list = []
	
	for s in samples:
		for i in range(all_data.shape[1]):
			result = {}
			result["name"] = names[i]
			result["incr"] = 0 
			result["per"] = pre_data[s][1]
			result["anch"] = 0

			val = all_data[s][i].round(0)
			change = val

	        # -- Identify Anchors --
			for an in range(5,9):
				col = pre_data[s][an]
				if (i == col):
					result["anch"] = 1

			# -- Find Change -- 
			for a in range(9,14):
				col = pre_data[s][a]
				if (i == col):

					new_sample_ind = int(transform[str(s)])
					idx = positions[new_sample_ind][col]
					increments = pre_data[s][a+5]
					change = bins_centred[i][int(idx+increments)]



			max_bin = np.max(bins_centred[i])
			min_bin = np.min(bins_centred[i])

			if (min_bin == -1):
				min_bin = 0

			if (max_bin < 10):
				max_bin = 10

			scl_val = ((val-min_bin)/(max_bin-min_bin)).round(2)
			scl_change = ((change-min_bin)/(max_bin-min_bin)).round(2)

			if (scl_val < 0 ):
				scl_val = 0
			if (scl_change < 0):
				scl_change = 0

			result["val"] = int(val)
			result["scl_val"] = scl_val
			result["change"] = int(change)
			result["scl_change"] = scl_change

			single_dict_list.append(result)
			
		final_data.append(single_dict_list)

	return final_data




changes = get_change_samples("pre_data1.csv","final_data_file.csv",3,4)

vals = pd.read_csv("final_data_file.csv",header=None).values
X = vals[:,1:]
y = vals[:,0]

X_no_9 = prepare_for_analysis("final_data_file.csv")[:,1:]

no_samples, no_features = X.shape

trans_dict = sample_transf(X)

bins_centred, X_pos_array, init_vals = divide_data_bins(X_no_9,[9,10])

testing = prep_for_D3_global("pre_data1.csv","final_data_file.csv",changes, bins_centred, X_pos_array,trans_dict)
testing = testing[:10]
