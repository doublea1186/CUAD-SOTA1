# -*- coding: utf-8 -*-
"""## Imports"""
import number_processing
from constants import date_question, period_question
import numpy as np
import pandas as pd
import statistics
import re
import argparse
import os


"""## Inputs"""
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--preds", type = str, default = "y_pred_base.csv",
                help = "path to predicted values")
ap.add_argument("-t", "--truths", type = str, default = "y_true.csv",
                help = "path to truth values")
args = vars(ap.parse_args())

y_pred_file = args["preds"]
y_pred = pd.read_csv(y_pred_file, header = 0)
#y_pred = y_pred[:5]

y_true_file = args["truths"]
y_true = pd.read_csv(y_true_file, header = 0)
# y_true = y_true[:5]


"""## Calculations"""
date_cols = []
period_cols = []
for q in date_question:
  date_cols.append(y_pred.columns.get_loc(q))
for q in period_question:
  period_cols.append(y_pred.columns.get_loc(q))

def findCommon(pred, comparison):
  return len(list(set(pred).intersection(comparison)))

def cleanupstring(s):
  out_s = s
  while '  ' in out_s:
      out_s = out_s.strip().replace('  ', ' ')
  return out_s, len(s)-len(out_s)

def calculateF1(str1, str2):
  str1 = re.sub(r'\W+', '', str1)
  str2 = re.sub(r'\W+', '', str2)
  numCommon = findCommon(str1, str2)
  if ((len(str1) == 0 and len(str2) != 0) or (len(str1) != 0 and len(str2) == 0)):
    return 0.0
  precision = (1.0 * numCommon) / (len(str1))
  recall = (1.0 * numCommon) / (len(str2))
  f1 = 0.0
  if ((precision + recall) != 0.0):
    f1 = (2 * precision * recall) / (precision + recall)
  return f1

f1 = []
for i in range(0, len(y_pred)):
  scores = []
  pred = y_pred.iloc[[i]].squeeze().tolist()
  true = y_true.iloc[[i]].squeeze().tolist()
  for j in range(0, len(pred)):
    if (isinstance(pred[j], str) and isinstance(true[j], str)):
      score = 0.0
      if (j in date_cols):
        d1 = number_processing.process_date(pred[j])
        d2 = number_processing.process_date(true[j])
        score = float(d1 == d2)
      elif (j in period_cols):
        d1 = number_processing.process_date(pred[j])
        d2 = number_processing.process_date(true[j])
        score = float(d1 == d2)
      else:
        score = calculateF1(pred[j], true[j])
      scores.append(score)
  f1.append(statistics.mean(scores))

print("Macro-Averaged F1 Score:")
print(statistics.mean(f1))