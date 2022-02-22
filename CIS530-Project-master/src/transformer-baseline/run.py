import pandas as pd 
import numpy as np 
from numba import prange
import json
import time 
import os
import gc

from transformers import pipeline

skip_file = ['VerizonAbsLlc_20200123_8-K_EX-10.4_11952335_EX-10.4_Service Agreement', 'AzulSa_20170303_F-1A_EX-10.3_9943903_EX-10.3_Maintenance Agreement1']
# 511 documents
# 41 questions

def compute_predictions(model, data, start, end, pred_data_path, score_data_path):
    columns = [
    'Title', 'Document Name', 'Parties', 'Agreement Date', 'Effective Date', 'Expiration Date', 'Renewal Term',
    'Notice to Terminate Renewal', 'Governing Law', 'Most Favored Nation', 'Non-Compete', 'Exclusivity',
    'No-Solicit of Customers', 'Competitive Restriction Exception', 'No-Solicit of Employees', 'Non-Disparagement',
    'Termination for Convenience', 'Right of First Refusal, Offer or Negotiation (ROFR/ROFO/ROFN)',
    'Change of Control', 'Anti-Assignment', 'Revenue/Profit Sharing', 'Price Restriction', 'Minimum Commitment',
    'Volume Restriction', 'IP Ownership Assignment', 'Joint IP Ownership', 'License Grant', 'Non-Transferable License',
    'Affiliate IP License-Licensor', 'Affiliate IP License-Licensee', 'Unlimited/All-You-Can-Eat License',
    'Irrevocable or Perpetual License', 'Source Code Escrow', 'Post-Termination Services', 'Audit Rights',
    'Uncapped Liability', 'Cap on Liability', 'Liquidated Damages', 'Warranty Duration', 'Insurance', 
    'Covenant Not to Sue', 'Third Party Beneficiary'
    ]
    size = end - start
    pred_data = pd.DataFrame(np.zeros((size, 42)), columns=columns)
    score_data = pd.DataFrame(np.zeros((size, 42)), columns=columns)

    for i in range(start, end):
        
        data = cuad_json['data'][i]
        title = data['title']
        if title in skip_file:
            continue
        print(f"processing {title}")
        context = data['paragraphs'][0]['context']
        lines = context.split('\n')
        if len(lines) > 1000:
            continue
        pred_data.iloc[i-start, 0] = title
        score_data.iloc[i-start, 0] = title

        start_time = time.time()
        # datapoints = []

        for j in range(len(data['paragraphs'][0]['qas'])):
            row = data['paragraphs'][0]['qas'][j]
            question = row['question']
            # datapoints.append({'question': question, 'context': context})
            datapoint = {'question': question, 'context': context}
            res = model(datapoint)
            score, pred_answer = res['score'], res['answer']
            pred_data.iloc[i-start, j+1] = pred_answer 
            score_data.iloc[i-start, j+1] = score

        end_time = time.time()

        print(f"finish processing {title} in {end_time - start_time}")
        pred_data.to_csv(pred_data_path)
        score_data.to_csv(score_data_path)
        gc.collect()

    # return pred_data, score_data 

if __name__ == "__main__":
    data_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../../data/"))
    input_file = os.path.join(data_dir, 'CUAD_v1/CUAD_v1.json')
    transformer_data_dir = os.path.join(data_dir, "transformer")

    model = pipeline('question-answering', device=0)
    f = open(input_file, 'r')
    cuad_json = json.load(f)

    start_times = list(range(0, 520, 10))
    interval = 10

    for i in range(51, len(start_times)):
      pred_file_name = os.path.join(transformer_data_dir, f"pred_data_{i}.csv")
      score_file_name = os.path.join(transformer_data_dir, f"score_data_{i}.csv")
      start = start_times[i]
      compute_predictions(model, cuad_json, start, start+interval, pred_file_name, score_file_name)
