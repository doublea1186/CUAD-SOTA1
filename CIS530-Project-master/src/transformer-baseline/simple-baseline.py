import pandas as pd
import os 
from number_processing import process_period, process_date 
from constants import *

# For simple baseline, just consiter renewal term as a period question

def format_date_answer(answer):
    return str(process_date(answer))

def format_period_answer(answer):
    time, unit = process_period(answer)
    if time is None or unit is None:
        return ""
    return f"{time} {unit}"

def format_boolean_answer(answer_prob, threshold=0.4):
    if answer_prob > threshold:
        return True
    else:
        return False

def get_question_type(question_name):
    if question_name in date_question:
        return "date"
    if question_name in period_question:
        return "period"
    return "span"

def unify_answers(pred_data):
    cleaned_answer = {}
    for question in pred_data.columns:
        question_type = get_question_type(question)
        answers = []
        for ct, answer in enumerate(pred_data[question]):
            if answer == "0.0":
                new_answer = ""
            elif question_type == "span":
                new_answer = answer
            elif question_type == "date":
                new_answer = format_date_answer(answer)
            elif question_type == "period":
                new_answer = format_period_answer(answer)
            answers.append(new_answer)
        cleaned_answer[question] = answers
    return cleaned_answer

if __name__ == "__main__":
    csv_file_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../data/transformer"))
    pred_date_path = os.path.join(csv_file_dir, "pred_data_final.csv")
    score_data_path = os.path.join(csv_file_dir, "score_data_final.csv")
    gt_data_path = os.path.join(csv_file_dir, "master_clauses.csv")
    unified_data_path = os.path.join(csv_file_dir, "unified.csv")

    pred_data = pd.read_csv(pred_date_path, index_col=0)
    score_data = pd.read_csv(score_data_path, index_col=0)
    gt_data = pd.read_csv(gt_data_path, index_col=0)
    unified_answer = unify_answers(pred_data)
    unified_df = pd.DataFrame(unified_answer)
    unified_df.to_csv(unified_data_path)

    print('end')
