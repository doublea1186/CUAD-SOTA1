# Imports
import numpy as np
import pandas as pd
import statistics
import re
import argparse
import os


# Argument Parser
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--preds", type = str, default = "y_pred_qdgat.csv",
                help = "path to predicted values")
ap.add_argument("-t", "--truths", type = str, default = "y_true_bool.csv",
                help = "path to truth values")
ap.add_argument("-o", "--output", type = str, default = "y_pred_new.csv",
                help = "path to output csv file")
args = vars(ap.parse_args())
y_pred_file = args["preds"]
y_true_file = args["truths"]
y_new_file = args["output"]


# Document Filter
drop_rows = ['Title', 'Document Name', 'Parties', 'Agreement Date', 'Effective Date',
			'Expiration Date', 'Renewal Term', 'Notice Period To Terminate Renewal', 'Governing Law']

y_pred = pd.read_csv(y_pred_file, encoding = 'unicode_escape', header = 0)
y_pred = y_pred.drop(drop_rows, axis = 1)

y_true = pd.read_csv(y_true_file, encoding = 'unicode_escape', header = 0)
y_true = y_true.drop(drop_rows, axis = 1)


# Concatenate Datasets
cols = y_pred.columns
data = [] # in the form of (str, bool)
for i in range(0, len(y_pred)):
	scores = []
	pred = y_pred.iloc[[i]].squeeze().tolist()
	true = y_true.iloc[[i]].squeeze().tolist()
	for j in range(0, len(pred)):
		questionText = cols[j]
		answerText = ''
		if (isinstance(pred[j], str) and len(pred[j]) > 0):
			answerText = pred[j]
		text = questionText + ' ' + answerText
		output = 1 if true[j] == 'Yes' else 0
		data.append([text, output])


# Convert Combined Dataset
df = pd.DataFrame(data, columns = ['Text', 'Output'])
df.to_csv(y_new_file, index = False)
