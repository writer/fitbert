import re

abbr_dict = {
    "what's": "what is",
    "what're": "what are",
    "who's": "who is",
    "who're": "who are",
    "where's": "where is",
    "where're": "where are",
    "when's": "when is",
    "when're": "when are",
    "how's": "how is",
    "how're": "how are",
    "i'm": "i am",
    "we're": "we are",
    "you're": "you are",
    "they're": "they are",
    "it's": "it is",
    "he's": "he is",
    "she's": "she is",
    "that's": "that is",
    "there's": "there is",
    "there're": "there are",
    "i've": "i have",
    "we've": "we have",
    "you've": "you have",
    "they've": "they have",
    "who've": "who have",
    "would've": "would have",
    "not've": "not have",
    "i'll": "i will",
    "we'll": "we will",
    "you'll": "you will",
    "he'll": "he will",
    "she'll": "she will",
    "it'll": "it will",
    "they'll": "they will",
    "isn't": "is not",
    "wasn't": "was not",
    "aren't": "are not",
    "weren't": "were not",
    "can't": "can not",
    "couldn't": "could not",
    "don't": "do not",
    "didn't": "did not",
    "shouldn't": "should not",
    "wouldn't": "would not",
    "doesn't": "does not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "won't": "will not",
    "[^\x00-\x7F]+": " ",
    "\s+": " ",
}


def sanitize_text(sentence):
    for key in abbr_dict:
        sentence = re.sub(key, abbr_dict[key], sentence, flags=re.IGNORECASE)
    sentence = sentence[0].upper() + sentence[1:]
    return sentence


def is_valid_sentence(sentence):
    return not "..." in sentence


def format_gap_task(masked_sentence, answer, options, gap_type):
    if not masked_sentence is None:
        gap_data = {}
        gap_data["question"] = masked_sentence
        gap_data["options"] = []
        for option in options:
            gap_data["options"].append(
                {"answer": option, "is_correct": option == answer}
            )
        gap_data["type"] = gap_type
        return gap_data
    else:
        return None
