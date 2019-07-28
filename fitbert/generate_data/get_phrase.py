import re

dictionary = {
    "NOUN": "a",
    "ADV": "b",
    "AUX": "c",
    "PART": "d",
    "ADP": "e",
    "PUNCT": "f",
    "ADJ": "g",
    "VERB": "h",
    "DET": "i",
    "PROPN": "j",
    "PRON": "k",
    "SYM": "l",
    "CCONJ": "m",
    "NUM": "n",
    "SPACE": "o",
    "INTJ": "p",
    "X": "x",
}

patterns_pos = {
    "NP": r"<DET>? <NUM>* (<ADJ> <PUNCT>? <CCONJ>?)* (<NOUN>|<PROPN> <PART>?)+",
    "PP": r"<ADP> <DET>? <NUM>* (<ADJ> <PUNCT>? <CCONJ>?)* (<NOUN> <PART>?)+",
    "VP": r"<AUX>* <ADV>* <VERB>",
}

patterns_code = {
    "NP": r"i?n*(gf?m?)*(a|jd?)+",
    "PP": r"ei?n*(gf?m?)*(ad?)+",
    "VP": r"h?b*h+",
}


def encode(pos_seq):
    code = ""
    for s in pos_seq:
        if s in dictionary:
            code += dictionary[s]
        else:
            code += "x"
    return code


def get_verb_phrase(sentence_span):
    verb_phrases = []
    code = encode([token.pos_ for token in sentence_span])
    for m in re.finditer(patterns_code["VP"], code):
        start = m.start()
        end = m.end()
        phrase_span = sentence_span[start:end]
        adv = [token for token in phrase_span if token.pos_ == "ADV"]
        main_verb = [
            token
            for token in phrase_span
            if (
                token.dep_ != "aux" and token.dep_ != "auxpass" and token.pos_ == "VERB"
            )
        ]
        verb_phrases.append(
            {
                "verb_phrase": sentence_span[start:end],
                "main_verb": main_verb,
                "adverbs": adv,
                "start": start,
                "end": end,
            }
        )
    return verb_phrases


def get_noun_phrase(sentence_span):
    noun_phrases = []
    code = encode([token.pos_ for token in sentence_span])
    for m in re.finditer(patterns_code["NP"], code):
        start = m.start()
        end = m.end()
        phrase_span = sentence_span[start:end]
        main_noun = [token for token in phrase_span if token.pos_ == "NOUN"]  # check
        if len(main_noun):
            noun_phrases.append(
                {
                    "noun_phrase": sentence_span[start:end],
                    "main_noun": main_noun,
                    "start": start,
                    "end": end,
                }
            )
    return noun_phrases
