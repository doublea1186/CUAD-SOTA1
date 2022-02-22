import os
import pandas as pd
import ast
import json
import argparse
import sys
sys.path.insert(0, '../')
from number_processing import *

def clean_up_list(list_string):
    if not type(list_string) == str:
        return list_string

    if not list_string[0] == '[' and ']':
        return list_string

    # assume no ' occurs in the real text
    # list_string = list_string[1:-1].replace("'", "")
    # res = [s.strip() for s in list_string.split(',')]
    try:
        res = ast.literal_eval(list_string)
    except (SyntaxError, ValueError):
        return list_string

    return res


def clean_task_name(task_name):
    cleaned_task_name = task_name.strip()
    cleaned_task_name = ' '.join(cleaned_task_name.split('_'))
    cleaned_task_name = cleaned_task_name.replace(' ', '_')
    cleaned_task_name = cleaned_task_name.replace('&', '_')
    cleaned_task_name = cleaned_task_name.replace("'", '_')
    cleaned_task_name = cleaned_task_name.replace('(', '')
    cleaned_task_name = cleaned_task_name.replace(')', '')
    return cleaned_task_name


def pair_qa(qa_df):
    question_and_answers = {}

    for index, row in qa_df.iterrows():
        qa = {}
        qa["file_name"] = row["Filename"]

        qa["questions"] = {}

        qa["questions"]["document_name"] = {}
        qa["questions"]["document_name"]["answer"] = clean_up_list(row["Document Name"])
        qa["questions"]["document_name"]["explanation"] = clean_up_list(row["Document Name"])

        qa["questions"]["parties"] = {}
        qa["questions"]["parties"]["answer"] = clean_up_list(row["Parties"])
        qa["questions"]["parties"]["explanation"] = clean_up_list(row["Parties"])

        qa["questions"]["effective_date"] = {}
        qa["questions"]["effective_date"]["answer"] = clean_up_list(row["Effective Date-Answer"])
        qa["questions"]["effective_date"]["explanation"] = clean_up_list(row["Effective Date"])

        qa["questions"]["expiration_date"] = {}
        qa["questions"]["expiration_date"]["answer"] = clean_up_list(row["Expiration Date-Answer"])
        qa["questions"]["expiration_date"]["explanation"] = clean_up_list(row["Expiration Date"])

        qa["questions"]["agreement_date"] = {}
        qa["questions"]["agreement_date"]["answer"] = clean_up_list(row["Agreement Date-Answer"])
        qa["questions"]["agreement_date"]["explanation"] = clean_up_list(row["Agreement Date"])

        qa["questions"]["renewal_term"] = {}
        qa["questions"]["renewal_term"]["answer"] = clean_up_list(row["Renewal Term-Answer"])
        qa["questions"]["renewal_term"]["explanation"] = clean_up_list(row["Renewal Term"])

        qa["questions"]["notice_period_to_terminate_renewal"] = {}
        qa["questions"]["notice_period_to_terminate_renewal"]["answer"] = clean_up_list(
            row["Notice Period To Terminate Renewal- Answer"])
        qa["questions"]["notice_period_to_terminate_renewal"]["explanation"] = clean_up_list(
            row["Notice Period To Terminate Renewal"])

        qa["questions"]["governing_law"] = {}
        qa["questions"]["governing_law"]["answer"] = clean_up_list(row["Governing Law"])
        qa["questions"]["governing_law"]["explanation"] = clean_up_list(row["Governing Law"])

        # qa["most_favoured_nation"] = row["Most Favored Nation-Answer"]
        # qa["competitive_restriction_execption"] = row["Competitive Restriction Exception-Answer"]
        # qa["non_compete"] = row["Non-Compete-Answer"]
        # qa["exclusivity"] = row["Exclusivity-Answer"]
        question_and_answers[clean_task_name(row["Filename"][:-4])] = qa

    return question_and_answers


def get_question_and_answers(csv_path):
    with open(csv_path, 'r') as qa_file:
        qa_df = pd.read_csv(qa_file)

    answers = pair_qa(qa_df)
    return answers


def get_qa(question, answer, filename):
    qa = dict()
    qa['question'] = question
    qa['answer'] = {}
    qa['query_id'] = filename + '_' + question

    qa['answer']['number'] = ''

    qa['answer']['date'] = {}
    qa['answer']['date']['day'] = ''
    qa['answer']['date']['month'] = ''
    qa['answer']['date']['year'] = ''

    qa['answer']['spans'] = []

    qa['answer']['period'] = {}
    qa['answer']['period']['time'] = ''
    qa['answer']['period']['unit'] = ''

    if question in ['document_name', 'parties', 'governing_law']:
        if answer is not None:
            if isinstance(answer, list):
                qa['answer']['spans'] = answer
            else:
                qa['answer']['spans'].append(answer)

    elif question in ['notice_period_to_terminate_renewal', 'renewal_term']:
        if answer is not None:
            if isinstance(answer, list) or pd.isna(answer):
                return qa

            time, unit = process_period(answer)
            qa['answer']['period']['time'] = time
            qa['answer']['period']['unit'] = unit


    elif question in ['agreement_date', 'effective_date', 'expiration_date']:
        if answer is not None:
            if pd.isna(answer):
                return qa

            date = answer.strip().split('/')
            if len(date) == 3:
                if date[0] != '[]':
                    qa['answer']['date']['month'] = date[0]
                if date[1] != '[]':
                    qa['answer']['date']['day'] = date[1]
                if date[2] != '[]':
                    qa['answer']['date']['year'] = date[2]
    return qa


def generate_drop_data(txt_data, csv_data):
    js_data = txt_data
    for filename in txt_data.keys():
        csv_filename = filename
        for question in csv_data[csv_filename]['questions']:
            js_data[filename]['qa_pairs'].append(
                get_qa(question, csv_data[csv_filename]['questions'][question]['answer'], filename))
    return js_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", type=str, default='./CUAD_v1/master_clauses.csv')
    parser.add_argument("--txt_path", type=str, default='./CUAD_v1/full_contract_txt')
    args = parser.parse_args()

    csv_path = args.csv_path
    txt_base_dir = args.txt_path

    ans = get_question_and_answers(csv_path)
    txt_file_list = os.listdir(txt_base_dir)
    js_data = {}
    for filename in txt_file_list:
        if filename[0] == '.':
            continue
        qa = {}
        qa['passage'] = ''
        qa['qa_pairs'] = []
        file_dir = os.path.join(txt_base_dir, filename)
        with open(file_dir, encoding="latin-1") as f:
            passage = f.read()
            qa['passage'] = passage
        js_data[clean_task_name(filename[:-4])] = qa

    drop_js = generate_drop_data(js_data, ans)
    js_dir = './cuad_dataset_number_(train or dev).json'
    with open(js_dir, 'w') as outfile:
        json.dump(drop_js, outfile, indent=4)


if __name__ == '__main__':
    main()
