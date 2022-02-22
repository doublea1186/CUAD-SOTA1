import csv
import pandas as pd
import argparse


def removesuffix(input_string, suffix):
    output_string = input_string
    if suffix and output_string.endswith(suffix):
        return output_string[:-len(suffix)]
    return output_string


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_path", type=str, default="./output/predictions.csv")
    args = parser.parse_args()
    pred_path = args.pred_path

    empty = None
    d = {'Document Name': empty, 'Parties': empty,
         'Agreement Date': empty, 'Effective Date': empty,
         'Expiration Date': empty, 'Renewal Term': empty,
         'Notice to Terminate Renewal': empty,
         'Governing Law': empty, 'Most Favored Nation': empty,
         'Non-Compete': empty, 'Exclusivity': empty,
         'No-Solicit of Customers': empty,
         'Competitive Restriction Exception': empty,
         'No-Solicit of Employees': empty, 'Non-Disparagement': empty,
         'Termination for Convenience': empty,
         'Right of First Refusal, Offer or Negotiation (ROFR/ROFO/ROFN)': empty,
         'Change of Control': empty, 'Anti-Assignment': empty,
         'Revenue/Profit Sharing': empty, 'Price Restriction': empty,
         'Minimum Commitment': empty, 'Volume Restriction': empty,
         'IP Ownership Assignment': empty, 'Joint IP Ownership': empty,
         'License Grant': empty, 'Non-Transferable License': empty,
         'Affiliate IP License-Licensor': empty,
         'Affiliate IP License-Licensee': empty,
         'Unlimited/All-You-Can-Eat License': empty,
         'Irrevocable or Perpetual License': empty,
         'Source Code Escrow': empty, 'Post-Termination Services': empty,
         'Audit Rights': empty, 'Uncapped Liability': empty, 'Cap on Liability': empty,
         'Liquidated Damages': empty, 'Warranty Duration': empty, 'Insurance': empty,
         'Covenant Not to Sue': empty, 'Third Party Beneficiary': empty}

    suffix_to_cat = {"_document_name": 'Document Name', "_parties": "Parties", "_agreement_date": "Agreement Date",
                     "_effective_date": "Effective Date", "_expiration_date": "Expiration Date",
                     "_renewal_term": "Renewal Term",
                     "_notice_period_to_terminate_renewal": "Notice to Terminate Renewal",
                     "_governing_law": "Governing Law"}

    suffix_list = ["_document_name", "_parties", "_agreement_date", "_effective_date", "_expiration_date",
                   "_renewal_term", "_notice_period_to_terminate_renewal", "_governing_law"]
    file = open(pred_path)
    csvreader = csv.reader(file)
    title_dict = {}

    for row in csvreader:
        if len(row) != 0:
            title = row[0].strip()

            for suffix in suffix_list:
                if title.endswith(suffix):
                    new_title = removesuffix(title, suffix)
                    if new_title not in title_dict.keys():
                        title_dict[new_title] = d.copy()
                    title_dict[new_title][suffix_to_cat[suffix]] = row[1]

    df = pd.DataFrame.from_dict(title_dict, orient='index')
    df.index.name = 'Title'
    df = df.reset_index()
    df.to_csv('./output/QDGAT_predictions_unified.csv')


if __name__ == '__main__':
    main()
