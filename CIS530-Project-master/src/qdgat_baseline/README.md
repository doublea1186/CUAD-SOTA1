# Overview
QDGAT(Question Directed Graph Attention Network for Numerical Reasoning over Text) with Date/Period Calculations.
# Prepare:
- Download the CoreNLP tools from https://stanfordnlp.github.io/CoreNLP/
- Navigate to `./qdgat_baseline` folder
- Use `json_generator.py` to collect passage-question-answer information to generate the .json file for annotation. Make sure to change the file name to `dev` or `train`.
- Start the CoreNLP server by running `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 50000 -maxCharLength 500000`
Since the passage is very long, you may have to tweak the `-timeout` value.
- Use the script `stanford_ner.py` to annotate the input json file
- Move the annotated json files into `../../../data/QDGAT` folder
# Usage:
- To train and evaluate, execute the `run.sh` or run `main.py` with appropriate arguments as clearly decribed in the file.
- After evaluation, a `predictions.csv` file will be saved to `./output` folder.
- You can also do evluation from a previous checkpoint by excuting `eval.sh` or run `main.py` spcifiying `--pre_path` as `"output"`