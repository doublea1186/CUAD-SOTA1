import re
import inflect
from constants import nlp
from word2number import w2n

class RegexGenerator():

    def __init__(self) -> None:
        self.engine = inflect.engine()

    def regex_relax_unit(self, s):
        word = s.lower()
        plural = self.engine.plural(word)
        start = f"[{s[0].upper()}|{s[0].lower()}]"
        unit = f"(?:{start + s[1:]})|(?:{start + plural[1:]})"
        return unit

section_kw = "\s([0-9]{1,2})\.\s"
subsection_kw = "\s([0-9]+\.[0-9]+)\s"
description_kw = "\((?:[^\(\)]*?)\"(.*?)\"\)"
bullet_alphabet_kw = "\s(\([a-z]\))\s"
colon_kw = "((?:(?!  +).)*):((?:(?!  +).)*)"
bullet_roman_number_kw = "\s(\((?:[Ii][XxVv]|[Vv]?[Ii]{0,3})\))\s"
srl_kw = "\[(?:B-|I-)?(?:R-|C-)?((?:[A-Z]|[0-9]|-)+?):(.+?)\]"

regex_generator = RegexGenerator()
time_units = ["second", "minute", "hour", "day", "week", "month", "year", "decade"]
time_bracket_kws = { unit: f"\(([a-zA-Z0-9]+)\) (?:{regex_generator.regex_relax_unit(unit)})" for unit in time_units }
time_kws = { unit: f"\(?([a-zA-Z0-9]+)\)? (?:{regex_generator.regex_relax_unit(unit)})" for unit in time_units }


def get_token_for_char(doc, char_idx):
    for i, token in enumerate(doc):
        token_start = token.idx
        token_end = token_start + len(token)

        if char_idx >= token_end:
            # find next token
            continue
        elif char_idx >= token_start and char_idx < token_end:
            return i
        else:
            # Maybe at a blank after a token
            return i

    return i

def generate_tuple(doc, text, regex_result, position):
    start_char_id = regex_result.start(position)
    end_char_id = regex_result.end(position)
    text_string = text[start_char_id: end_char_id]
    stripped_string = text_string.strip()
    if stripped_string == '':
        start_token_id = get_token_for_char(doc, start_char_id)
        end_token_id = get_token_for_char(doc, end_char_id - 1) + 1
        string_form = doc[start_token_id: end_token_id]
        return start_token_id, end_token_id, string_form

    # Remove trailing spaces
    start_offset = 0
    end_offset = 0

    for ct, char in enumerate(text_string):
        if char == stripped_string[0]:
            start_offset = ct
            break

    for ct, char in enumerate(reversed(text_string)):
        if char == stripped_string[-1]:
            end_offset = ct
            break

    start_char_id += start_offset
    end_char_id -= end_offset

    start_token_id = get_token_for_char(doc, start_char_id)
    end_token_id = get_token_for_char(doc, end_char_id - 1) + 1
    string_form = doc[start_token_id: end_token_id]
    return start_token_id, end_token_id, string_form

def get_hierachy_tuples(doc):
    text = str(doc)
    sections = [(get_token_for_char(doc, m.start(1)), get_token_for_char(doc, m.end(1) - 1) + 1, text[m.start(1): m.end(1)]) for m in re.finditer(section_kw, text)]
    subsections = [(get_token_for_char(doc, m.start(1)), get_token_for_char(doc, m.end(1) - 1) + 1, text[m.start(1): m.end(1)])  for m in re.finditer(subsection_kw, text)]
    bullet_alphabets = [(get_token_for_char(doc, m.start(1)), get_token_for_char(doc, m.end(1) - 1) + 1, text[m.start(1): m.end(1)])  for m in re.finditer(bullet_alphabet_kw, text)]
    bullet_roman_number = [(get_token_for_char(doc, m.start(1)), get_token_for_char(doc, m.end(1) - 1) + 1, text[m.start(1): m.end(1)])  for m in re.finditer(bullet_roman_number_kw, text)]

    return sections, subsections, bullet_alphabets, bullet_roman_number

def get_colon_tuples(doc):
    text = str(doc)
    definitions = [generate_tuple(doc, text, m, 1) for m in re.finditer(colon_kw, text)]
    explanations = [generate_tuple(doc, text, m, 2) for m in re.finditer(colon_kw, text)]
    return definitions, explanations

def get_hierachy(text):
    sections = [text[m.start(1): m.end(1)] for m in re.finditer(section_kw, text)]
    subsections = [text[m.start(1): m.end(1)]  for m in re.finditer(subsection_kw, text)]
    bullet_alphabets = [text[m.start(1): m.end(1)]  for m in re.finditer(bullet_alphabet_kw, text)]
    bullet_roman_number = [text[m.start(1): m.end(1)]  for m in re.finditer(bullet_roman_number_kw, text)]
    return sections, subsections, bullet_alphabets, bullet_roman_number

def get_bracket_alias_tuples(doc):
    text = str(doc)
    bracket_alias = [(get_token_for_char(doc, m.start(1)),
                      get_token_for_char(doc, m.end(1) - 1) + 1,
                      text[m.start(1): m.end(1)]) for m in re.finditer(description_kw, text)]
    return bracket_alias

def get_bracket_alias(text):
    bracket_alias = [text[m.start(1): m.end(1)] for m in re.finditer(description_kw, text)]
    return bracket_alias

def get_bracket_time_tuples(doc):
    text = str(doc)
    times = {}
    for time_unit, time_kw in time_bracket_kws.items():
        bracket_time = []
        for m in re.finditer(time_kw, text):
            try:
                number = w2n.word_to_num(text[m.start(1): m.end(1)])
                start = get_token_for_char(doc, m.start(1))
                end = get_token_for_char(doc, m.end(1) - 1) + 1
                bracket_time.append((start, end, number))
            except ValueError:
                continue
        if not len(bracket_time) == 0:
            times[time_unit] = bracket_time
    return times

def get_time(text):
    times = {}
    for time_unit, time_kw in time_kws.items():
        bracket_time = []
        for m in re.finditer(time_kw, text):
            try:
                number = w2n.word_to_num(text[m.start(1): m.end(1)])
                bracket_time.append(number)
            except ValueError:
                continue
        # bracket_time = [w2n.word_to_num(text[m.start(1): m.end(1)]) for m in re.finditer(time_kw, text)]
        if not len(bracket_time) == 0:
            times[time_unit] = bracket_time
    return times

def get_srl_tuples(text):
    srl_tuples = re.findall(srl_kw, text)
    return srl_tuples

if __name__ == "__main__":
    text = '''
Exhibit 99.3

EXECUTION COPY

INTELLECTUAL PROPERTY AGREEMENT

THIS INTELLECTUAL PROPERTY AGREEMENT (this "Intellectual Property Agreement"), dated as of December 20, 2007, is made by and between NMS COMMUNICATIONS CORP., a Delaware corporation ("Seller"), and VERSO BACKHAUL SOLUTIONS, INC., a Georgia corporation ("Backhaul").

RECITALS:

WHEREAS, Seller and Verso Technologies, Inc., a Minnesota corporation ("Buyer"), have entered into that certain Asset Purchase Agreement, dated as of the date hereof (the "Asset Purchase Agreement"), pursuant to which Buyer has the right to acquire the Purchased Assets of Seller and its Subsidiaries, as more particularly described in the Asset Purchase Agreement (all capitalized words and terms used herein and not otherwise defined herein shall have the meanings ascribed to them in the Asset Purchase Agreement); and

WHEREAS, Buyer has designated Backhaul as a Buyer Designee for purposes of the Asset Purchase Agreement, and Buyer has assigned to Backhaul the right to receive the Purchased Assets pursuant to that certain Assignment of Asset Purchase Agreement between Buyer and Backhaul dated as of the date hereof.

ASSIGNMENT:

NOW, THEREFORE, for good and valuable consideration, the receipt and adequacy of which are hereby acknowledged, Seller does hereby transfer, sell, assign, convey and deliver to Backhaul all right, title and interest in, to and under the Assigned Intellectual Property, including, without limitation, the Trademarks and Patents set forth on Schedules A and B hereof, respectively, and all goodwill of the Purchased Business associated therewith. Seller hereby covenants and agrees, that from time to time forthwith upon the reasonable written request of Backhaul or Buyer, that Seller will, at Backhaul's cost and expense, do, execute, acknowledge and deliver or cause to be done, executed, acknowledged and delivered, each and all of such further acts, deeds, assignments, transfers, conveyances and assurances as may reasonably be required by Backhaul or Buyer in order to transfer, assign, convey and deliver unto and vest in Backhaul title to all right, title and interest of Seller in, to and under the Assigned Intellectual Property.

This Intellectual Property Agreement is subject in all respects to the terms and conditions of the Asset Purchase Agreement and is intended only to document the assignment of the Assigned Intellectual Property. Nothing contained in this Intellectual Property Agreement shall be deemed to supersede any of the obligations, agreements, representations, covenants or warranties of Seller and Buyer contained in the Asset Purchase Agreement.

This Intellectual Property Agreement shall be construed and interpreted according to the laws of the State of Georgia, applicable contracts to be wholly performed within the State of Georgia.







This Intellectual Property Agreement may be executed in one or more counterparts, and by the different parties hereto in separate counterparts, each of which when executed shall be deemed to be an original, but all of which taken together shall constitute one and the same agreement. Delivery of an executed counterpart of a signature page to this Intellectual Property Agreement by facsimile shall be effective as delivery of a manually executed counterpart of this Intellectual Property Agreement.

[Signature Page to Follow]

2







IN WITNESS WHEREOF, the parties hereto have executed and delivered this Intellectual Property Agreement as of the date first written above.



  NMS COMMUNICATIONS CORP.       By: /s/ Robert Schechter       Name: Robert Schechter       Title: CEO/President             VERSO BACKHAUL SOLUTIONS, INC.       By: /s/ Martin D. Kidder       Name: Martin D. Kidder       Title: President







STATE OF Massachusetts:

COUNTY OF Middlesex:

On the 20th day of December, 2007, before me personally came Robert Schechter, to me known (or satisfactorily proven), who being by me duly sworn, did depose and say that he/she is the CEO/President of NMS Communications Corporation, the corporation described in, and which executed the foregoing instrument, and that he/she was fully authorized to execute this Intellectual Property Agreement on behalf of said corporation.



  /s/ Jason A. Minio (SEAL)       Jason A. Minio Notary Public Commonwealth of Massachusetts My Commission Expires November 1, 2013



STATE OF Georgia:

COUNTY OF Cobb:

On the 20th day of December, 2007, before me personally came Martin Kidder, to me known (or satisfactorily proven), who being by me duly sworn, did depose and say that he/she is the CFO of Verso Technologies, the corporation described in, and which executed the foregoing instrument, and that he/she was fully authorized to execute this Intellectual Property Agreement on behalf of said corporation.



  /s/ Susanne G. Davis (SEAL)       Susanne G. Davis Notary Public, Cobb County, GA My Commission expires Aug. 10, 2010









SCHEDULE A



[INTENTIONALLY OMITTED]







SCHEDULE B



[INTENTIONALLY OMITTED]
    '''
    doc = nlp(text)
    colon_explanations = get_colon_tuples(doc)
