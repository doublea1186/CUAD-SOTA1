
import string
import spacy

date_question = ["Agreement Date", "Effective Date", "Expiration Date",]
period_question = ["Renewal Term", "Notice to Terminate Renewal"]

nlp = spacy.load('en_core_web_lg')

ordinals = ["first", "1st"
"second", "2nd",
"third", "3rd",
"fourth", "4th",
"fifth", "5th",
"sixth", "6th",
"seventh", "7th",
"eighth", "8th",
"ninth", "9th",
"tenth", "10th",
"eleventh", "11th",
"twelfth", "12th",
"thirteenth", "13th",
"fourteenth", "14th",
"fifteenth", "15th",
"sixteenth", "16th",
"seventeenth", "17th",
"eighteenth", "18th",
"nineteenth", "19th",
"twentieth", "20th",
"twenty-first", "21st",
"twenty-second", "22nd",
"twenty-third", "23rd",
"twenty-fourth", "24th",
"twenty-fifth", "25th",
"twenty-sixth", "26th",
"twenty-seventh", "27th",
"twenty-eighth", "28th",
"twenty-ninth", "29th",
"thirtieth", "30th",
"thirty-first", "31st"]

year_nums = [str(i) for i in list(range(1900, 2100))]
date_nums = [str(i) for i in list(range(1, 32))]
# clarification = ['year', 'month', 'day']

date_normalization_kw = [
    "january", "jan",
    "february", "feb",
    "march", "mar",
    "april", "apr",
    "may",
    "june", "jun",
    "july", "jul",
    "august", "aug",
    "september", "sep",
    "october", "oct",
    "november", "nov",
    "december", "dec",
] + ordinals + year_nums + date_nums + ['.', ',', '/']
