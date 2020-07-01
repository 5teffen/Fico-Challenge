fp = open("flask_pre_data_4changes_no_top_fix.csv", 'r')
fp1 = open("pred_data_x.csv", 'w')

a = fp.readline()
fp1.write(a)

for i in range(10459):
	a = fp.readline()
	fp1.write(a[:-2])
	fp1.write('\n')

fp.close()
fp1.close()