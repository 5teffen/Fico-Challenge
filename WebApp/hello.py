from flask import Flask
from flask import request, jsonify, json, redirect
from flask import render_template
import pandas as pd
import numpy as np
from SVM_model import SVM_model
from Functions import *
from Text_Explanation import *
from ILE import *

np.random.seed(12345)


 
# ------- Helper functions ------- #

def display_data (sample):
	sample -= 1
	if X[sample][0] == -9:
		category = "NA"
		return sample, 0, 0, category, -1
	else:
		good_percent = svm_model.run_model(X[sample])
		predicted = 0
		if good_percent>.5:
			predicted = 1
		ground_truth = y[sample]
		model_correct = 1
		if predicted != ground_truth:
			model_correct = 0
		category = "NN";
		if (predicted, model_correct) == (0,0):
			category = "FN"
		elif (predicted, model_correct) == (0,1):
			category = "TN"
		elif (predicted, model_correct) == (1,0):
			category = "FP"
		elif (predicted, model_correct) == (1,1):
			category = "TP"
		return sample, good_percent, model_correct, category, predicted

trans_dict = {}
def sample_transf ():
	my_count = 0
	for sample in range(10459):
		if X[sample][0] != -9:
			trans_dict[str(sample)] = my_count
			my_count += 1
		else:
			trans_dict[str(sample)] = -9



# ------- Initialize model ------- #


vals = pd.read_csv("static/data/final_data_file.csv", header=None).values
X = vals[:,1:]
y = vals[:,0]

vals_no_9 = prepare_for_analysis("static/data/final_data_file.csv")
X_no_9 = vals_no_9[:,1:]

no_samples, no_features = X.shape

svm_model = SVM_model(None,"static/data/final_data_file.csv")
svm_model.train_model(0.001)
svm_model.test_model()

bins_centred, X_pos_array, init_vals = divide_data_bins(X_no_9,[9,10])
dict_array_orig = scaling_data_density(X_no_9, bins_centred, False)
dict_array_monot = scaling_data_density(X_no_9, bins_centred, True)
count_total = occurance_counter("static/data/pred_data_x.csv")
sample_transf()



# ------ Initialize WebApp ------- #

app = Flask(__name__) # static_folder="C:/Users/Oscar/Documents/UGR 2018/Fico-Challenge-master/VisualApp1/static")

@app.route('/')
def hello():
    return redirect("/intro")

@app.route('/intro')
def intro_site():
	return render_template("index_intro.html")


# ------- Individual Explanations ------- #

@app.route('/individual')
def ind_site():
    return render_template("index_individual.html")

@app.route('/instance', methods=['GET'])
def handle_request():

	np.random.seed(12345)

	if request.method == 'GET':
		sample = -10
		try:
			sample = int(request.args.get('sample'))
		except:
			return "Please enter a sample number in the range (1, 10459)."

		if sample != -10:
			if sample<1 or sample>10459:
				return "Please enter a sample number in the range (1, 10459)."
			else:			
				
				monot = (request.args.get('monot') == "True")
				sort = (request.args.get('sort') == "True")
				sample, good_percent, model_correct, category, predicted = display_data(sample)
				
				### Run MSC and Anchors
				trans_sample = trans_dict[str(sample)]
				change_vector, change_row, anchors, percent = instance_explanation(svm_model, X_no_9, X_no_9[trans_sample], trans_sample, X_pos_array, bins_centred)

				### Parse values into python dictionary
				ret_string = ""
				data_array = prepare_for_D3(X[sample], bins_centred, change_row, change_vector, anchors, percent, monot)

				dict_array = []
				if monot:
					dict_array = dict_array_monot
				else:
					dict_array = dict_array_orig

				if sort:
					data_array, dict_array = sort_by_val(data_array, dict_array)

				for dct in data_array:
					ret_string += json.dumps(dct)
					ret_string += "~"

				for dct in dict_array:
					ret_string += json.dumps(dct)
					ret_string += "~"

				text_exp = generate_text_explanation(good_percent, X[sample], change_row, change_vector , anchors)
				similar_ids = detect_similarities("static/data/pred_data_x.csv","static/data/final_data_file.csv", X[sample], change_row, bins_centred, good_percent)
				similar_ids = similar_ids[:min(len(similar_ids),10)]
				ret_string += json.dumps({'sample': sample+1, 'good_percent': good_percent, 'model_correct': model_correct,
										  'category': category, 'predicted': predicted, 'trans_sample': trans_sample,
										  'text_exp': text_exp, 'similar_ids': similar_ids})
				
				return ret_string



# ------- Global Explanations ------- #

@app.route('/glob_req')
def glob_site_bars():

	if request.method == 'GET':

		ret_arr = []
		arr = list (count_total)
		for item in arr:
			new_item = list(item)
			ret_arr.append(new_item)

		keyTots = []
		chgTots = []
		for i in range(no_features):
			keyTots.append(ret_arr[i][0]+ret_arr[i][1])
			chgTots.append(ret_arr[i][2]+ret_arr[i][3])


		keySort = sorted(range(len(keyTots)), key=lambda k: keyTots[k])[::-1]
		chgSort = sorted(range(len(chgTots)), key = lambda k: chgTots[k])[::-1]

		ret_arr = [keySort, chgSort, ret_arr]

		ret_string = json.dumps(ret_arr)

	return ret_string

@app.route('/global')
def glob_site():
	return render_template("index_global.html")

@app.route('/glob_feat', methods=['GET'])
def handle_request_mini_graphs():

	if request.method == 'GET':

		id_list = request.args.get('id_list').split(',')
		if not id_list[-1]:
			print("remove")
			id_list = id_list[:-1]

		# Cap number of minigraphs on right panel
		sample_cap = min(len(id_list), 30)
		id_list = [int(x) for x in id_list][:sample_cap]

		mini_graph_arr = prep_for_D3_global("static/data/pred_data_x.csv","static/data/final_data_file.csv", id_list, bins_centred, X_pos_array, trans_dict)

		## Parse values into python dictionary
		ret_string = [mini_graph_arr, id_list]
		ret_string = json.dumps(ret_string)

		return ret_string

@app.route('/first_panel', methods=['GET'])
def handle_request_ft():

	if request.method == 'GET':

		ft_list = request.args.get('features')
		ft_list = ft_list[1:-1].split(',')

		# False = changes, True = keyfts
		algorithm = (request.args.get('algorithm') == "True")

		if ft_list[0] == -1 or ft_list == ['']:
			return ""
		else:
			ft_list = [int(x) for x in ft_list]
			ft_list.sort()

		combinations = combination_finder("static/data/pred_data_x.csv",ft_list,algorithm)

		ret_arr = []
		if not algorithm:
			for combi in combinations[:min(15,len(combinations))]:
				ret_arr.append(changes_generator("static/data/pred_data_x.csv", combi))
		else:
			for combi in combinations[:min(15,len(combinations))]:
				ret_arr.append(anchor_generator("static/data/pred_data_x.csv","static/data/final_data_file.csv", combi))


		## Parse values into python dictionary
		ret_string = json.dumps(ret_arr)

		return ret_string



# ------- Run WebApp ------- #

if __name__ == '__main__':

	np.random.seed(12345)

	app.run(port=5005, host="0.0.0.0", debug=False)