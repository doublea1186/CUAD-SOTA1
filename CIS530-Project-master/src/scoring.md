## Evaluation Metric Scoring
The selected evaluation metric for the given problem is a Macro-Averaged F1 Score.


### Metric Overview
 Assume the following:
 * y_pred and y_true are a dataset wherein rows correspond to documents and columns correspond to questions. 
 * Each row-column entry representing the answer to a particular question with reference to a particular document.
 * y_pred represents the predictions made by the model while y_true reprents the ground truth values.

The Macro-Averaged F1 Score can then be calculated as follows:
1. For a given document, iterate through each question.
2. For each question, obtain both the predicted answer (refer to this as 'pred') and the ground truth value (refer to this as 'true').
3. For questions involving dates, we use a custom date parser to numeric representations of day, month and year for the answers. We do the same for questions inolving time periods, obtaining representations for time and unit for the answers. We then indicate a score of 1 if there is a match, and 0 if not.
4. For other questions, compute the string-based F-1 score between these two answers as follows:
	 * Precision = numCommon / number of tokens in pred.
	 * Recall = numCommon / number of tokens in true.
	 * F1 = (2 * Precision * Recall) / (Precision + Recall).
5. Obtain the average of the scores for each question within the document and append it to a list (f1Scores).
6. Calculate the Macro-Average F-1 Score by obtaining the average F-1 score over all documents, with the F1 score of each document being in the list f1Scores.


### Execution Instructions
Required Files:
* A file that contains question responses, separated by new lines. Let us refer to this as y-pred.
* A file that contains possible correct responses, separated by new lines, where each possible correct response is separated by a comma. Let us refer to this as y-true.
* score.py: Contains code for calculating the evaluation metric.
* score.py: Executable for calculating the evaluation metric on the existing prediction data.

To obtain predictions for a specific dataset, avigate to the directory in which score.py is and run the following in the terminal:
```
python score.py -p <path-to-y-pred> -t <path-to-y-true>
```

To obtain predictions for the given predictions, navigate to the directory in which score.py is and run the following in the terminal:
```
python score.py
```


### Example Execution
With the given y_pred.txt and y_true.txt files, the following can be run to test their performance on this metric:
```
python score.py -p y_pred.txt -t y_true.txt
```


### References
* Rajpurkar, P., et al. "SQuAD: 100,000+ questions for machine comprehension of text."  _Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing_, 2016, doi:10.18653/v1/d16-1264.
* Snow, Amie B., et al. "Evaluating The Effectiveness of a State-Mandated Benchmark Reading Assessment: mCLASS Reading 3D (Text Reading and Comprehension)."  _Reading Psychology_, vol. 39, no. 4, 2018, pp. 303-334.