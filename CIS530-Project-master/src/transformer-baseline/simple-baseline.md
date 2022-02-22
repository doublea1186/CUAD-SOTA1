# Overview
The weak baseline makes use of the hugging face transformer Model for question and answering.

# Prepare:
1. Setup the environment using conda with environment.yml at the root directory
`conda env create -f environment.yml`
2. Activate the environment by
`conda activate cuad_env`

# Usage:
- Navigate to `src/transformer_baseline` folder
- Use `simple-baseline.py` to predict the span form predicted answers, the output will be saved to `data/transformer/pred_data_<id>.csv`
- Use `combine.py` to combine multiple batches of question and answerings into a large file at `data/transformer/pred_data.csv`
- Use `post-processing.py` to unify the formatting of the answers to Date, Period, or maintain Span. The output will be saved to `data/transformer/pred_data_final.csv`