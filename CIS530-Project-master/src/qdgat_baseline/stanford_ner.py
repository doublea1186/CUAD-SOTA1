'''
A sample code usage of the python package stanfordcorenlp to access a Stanford CoreNLP server.
Written as part of the blog post: https://www.khalidalnajjar.com/how-to-setup-and-use-stanford-corenlp-server-with-python/ 
'''

from stanfordcorenlp import StanfordCoreNLP
import logging
import sys
import json
import argparse
from tqdm import tqdm
import os

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port, timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))

def annotate_text(snlp, text: str):
    "Annotate a piece of text."

    FLAG_NER = "tp@ckl"
    FLAG_SENTENCE = "tp#ckl"

    text = text.replace('%', '')
    
    try: #try parsing to dict
        annotations = json.loads(snlp.nlp.annotate(text, properties=snlp.props))
    except:
        print(repr(snlp.nlp.annotate(text, properties=snlp.props)))
        print(sys.exc_info())
    
    annotated_text = ""
    
    for sentence in annotations['sentences']:
        # tokens = list of dictionaries, each dictionary = token (word)
        for token in sentence['tokens']:
            if token['ner'] == 'O':
                annotated_text += token['word'] 
            else:
                annotated_text += token['word'] + FLAG_NER + token['ner'] + FLAG_NER 

            # append space, unless token is last token of the sentence
            annotated_text += " " if token['index'] != len(sentence['tokens']) else ""
        
        # append space, unless sentence is last sentence of the text
        annotated_text += FLAG_SENTENCE + " " if sentence['index'] != len(annotations['sentences']) else ""
    
    return annotated_text


def annotate_file(file_path):
    "Annotate the passages and corresponding questions of a DROP JSON file."
    print("1")
    # step 1: initialize annotator
    sNLP = StanfordNLP()
    print("2")
    # step 2: read in original DROP dataset
    with open(file_path) as dataset_file:
        dataset = json.load(dataset_file)
    
    # step 3: annotate all passages and the questions of all corresponding qa pairs
    for story in tqdm(dataset.keys()):
        passage = dataset[story]['passage'] # string
        # overwrite with annotated passage
        dataset[story]['passage'] = annotate_text(sNLP, passage)

        qa_pairs = dataset[story]['qa_pairs'] # list of dicts, each dict being a qa pair
        for idx, qa_pair in enumerate(qa_pairs):
            question = qa_pair['question']
            # overwrite with annotated question
            dataset[story]['qa_pairs'][idx]['question'] = annotate_text(sNLP, question)

    # step 4: save resulting dict as new json
    result_file_name = args.file_path[:-5] + "_parsed.json"
    with open(result_file_name, 'w') as f:
        json.dump(dataset, f)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    # Required parameters
    parser.add_argument(
        "--file_path",
        type=str,
        help="file you want to annotate",
    )

    args = parser.parse_args()
    print(args)
    annotate_file(args.file_path)

    #text = 'Beyonce lives in Los Angeles. I work in New York City.'

    #text = "Hoping to rebound from their loss to the Patriots, the Raiders stayed at home for a Week 16 duel with the Houston Texans.  Oakland would get the early lead in the first quarter as quarterback JaMarcus Russell completed a 20-yard touchdown pass to rookie wide receiver Chaz Schilens.  The Texans would respond with fullback Vonta Leach getting a 1-yard touchdown run, yet the Raiders would answer with kicker Sebastian Janikowski getting a 33-yard and a 30-yard field goal.  Houston would tie the game in the second quarter with kicker Kris Brown getting a 53-yard and a 24-yard field goal. Oakland would take the lead in the third quarter with wide receiver Johnnie Lee Higgins catching a 29-yard touchdown pass from Russell, followed up by an 80-yard punt return for a touchdown.  The Texans tried to rally in the fourth quarter as Brown nailed a 40-yard field goal, yet the Raiders' defense would shut down any possible attempt."
    #text = "How many field goals did Kris Brown kick?"

    #text = 'The first issue in 1942 consisted of denominations of 1, 5, 10 and 50 centavos and 1, 5, and 10 Pesos. The next year brought "replacement notes" of the 1, 5 and 10 Pesos while 1944 ushered in a 100 Peso note and soon after an inflationary 500 Pesos note. In 1945, the Japanese issued a 1,000 Pesos note. This set of new money, which was printed even before the war, became known in the Philippines as Mickey Mouse money due to its very low value caused by severe inflation. Anti-Japanese newspapers portrayed stories of going to the market laden with suitcases or "bayong" (native bags made of woven coconut or Corypha leaf strips) overflowing with the Japanese-issued bills. In 1944, a box of matches cost more than 100 Mickey Mouse pesos. In 1945, a kilogram of camote cost around 1000 Mickey Mouse pesos. Inflation plagued the country with the devaluation of the Japanese money, evidenced by a 60% inflation experienced in January 1944.'