import pandas as pd
import numpy as np
from SVM_model import SVM_model
from ILE import instance_explanation, prepare_for_D3, divide_data_bins
from Functions import prepare_for_analysis

np.random.seed(12345)

vals = pd.read_csv("final_data_file.csv", header=None).values
X = vals[:,1:]
y = vals[:,0]

vals_no_9 = prepare_for_analysis("final_data_file.csv")
X_no_9 = vals_no_9[:,1:]

no_samples, no_features = X.shape

svm_model = SVM_model(None,"final_data_file.csv")
svm_model.train_model(0.001)
svm_model.test_model()

bins_centred, X_pos_array, init_vals = divide_data_bins(X_no_9,[9,10])

# sample = 2
# print(X[sample])
# print(instance_explanation(svm_model, X, X[sample], sample, X_pos_array, bins_centred))
# print(instance_explanation(svm_model, X, X[sample], sample, X_pos_array, bins_centred))
# print(instance_explanation(svm_model, X, X[sample], sample, X_pos_array, bins_centred))
ANCH_THRESH = 4
CHG_THRESH = 5

print(X.shape)
print(X_no_9.shape)


print(np.random.normal())

fp = open("flask_pre_data_4changes_no_top_fix.csv", 'w')

fp.write("ID,Percentage,Category,no_Anch,no_Chg,Anch1,Anch2,Anch3,Anch4,Chg1,Chg2,Chg3,Chg4,Chg5,Hgt1,Hgt2,Hgt3,Hgt4,Hgt5\n")

# --- ID NUMBERS AND ANCHORS AMD CHANGES ARE INDEXED WITH 1 ---
my_count = 0
for sample in range(no_samples):

	np.random.seed(12345)

	# print(np.random.normal())
	

	fp.write(str(sample+1))
	fp.write(',')

	if sample%20 == 0:
		print(sample)

	if X[sample][0] == -9:
		fp.write("-9,")
		fp.write("NA,")
		fp.write("0,")
		fp.write("0,")
		for i in range(ANCH_THRESH+2*CHG_THRESH):
			fp.write("-9,")
		fp.write('\n')

	else:

		### Run MSC Algorithm 
		change_vector, change_row, anchors, percent = instance_explanation(svm_model, X_no_9, X_no_9[my_count], my_count, X_pos_array, bins_centred)

		predicted = 0
		if percent>.5:
			predicted = 1
		ground_truth = y[sample]
		model_correct = 1
		if predicted != ground_truth:
			model_correct = 0
		category = "NA";
		if (predicted, model_correct) == (0,0):
			category = "FN"
		elif (predicted, model_correct) == (0,1):
			category = "TN"
		elif (predicted, model_correct) == (1,0):
			category = "FP"
		elif (predicted, model_correct) == (1,1):
			category = "TP"

		try:
			anchors1 = list(anchors)
		except:
			pass
		try:
			change_vector1 = list(change_vector)
		except:
			pass
		
		fp.write(str(percent))
		fp.write(',')
		fp.write(str(category))
		fp.write(',')

		if (anchors is not None):
			anch_cnt = anchors1.count(1)
			fp.write(str(anch_cnt)+",")
		else:
			fp.write("0,")
		if (change_vector is not None):
			chg_cnt = 23 - change_vector1.count(0)
			fp.write(str(chg_cnt)+",")
		else:
			fp.write("0,")

		if (anchors is not None):
			for i in range(no_features):
				if anchors1[i] == 1:
					fp.write(str(i))
					fp.write(",")
			for i in range(ANCH_THRESH - anch_cnt):
				fp.write("-99")
				fp.write(",")
		else:
			for i in range(ANCH_THRESH):
				fp.write("-99")
				fp.write(",")

		if (change_vector is not None):
			for i in range(no_features):
				if change_vector1[i] != 0:
					fp.write(str(i))
					fp.write(",")
			for i in range(CHG_THRESH - chg_cnt):
				fp.write("-99")
				fp.write(",")

			for i in range(no_features):
				if change_vector1[i] != 0:
					fp.write(str(change_vector1[i]))
					fp.write(",")
			for i in range(CHG_THRESH - chg_cnt):
				fp.write("-99")
				fp.write(",")
		else:
			for i in range(CHG_THRESH*2):
				fp.write("-99")
				fp.write(",")

		my_count += 1


		fp.write('\n')

fp.close()