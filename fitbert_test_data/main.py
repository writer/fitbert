import argparse
import json

import pandas as pd
import spacy
from tqdm import tqdm

from get_gap import get_noun_gap, get_verb_gap
from utils import format_gap_task, is_valid_sentence, sanitize_text

nlp = spacy.load("en_core_web_sm")


def parse_args():
    parser = argparse.ArgumentParser(description="Create fill-in dataset.")
    parser.add_argument("input_file_path", help="file_path")
    parser.add_argument("output_file_path", help="output_file_path")
    parser.add_argument(
        "--max_count", "-m", help="max num of datapoints to generate", default=2000000
    )
    parser.add_argument(
        "--gap_type", "-t", help="type of datapoints: all, verb, tense", default="all"
    )
    parser.add_argument(
        "--mask_string",
        "-s",
        help="string to replace gap word, default is '***mask***'",
        default="***mask***",
    )
    args = parser.parse_args()
    return args


def main(args):

    input_file_path = args.input_file_path
    output_file_path = args.output_file_path
    max_count = int(args.max_count)
    gap_type = args.gap_type
    mask_string = args.mask_string

    dataset_df = pd.read_csv(input_file_path, encoding="ISO-8859-1")
    dataset_df = dataset_df[0:max_count]

    dataset_with_gaps = []

    for _, row in tqdm(dataset_df.iterrows(), total=len(dataset_df.index)):
        text = row["text"]
        doc = nlp(text)
        for sentence in doc.sents:

            if is_valid_sentence(sentence.text):

                sentence_sanitized = nlp(sanitize_text(sentence.text))

                if gap_type == "all" or gap_type == "noun":
                    masked_sentence, answer, options = get_noun_gap(
                        sentence_sanitized, mask_string
                    )
                    gap_data = format_gap_task(masked_sentence, answer, options, "noun")
                    if not gap_data is None:
                        dataset_with_gaps.append(gap_data)

                if gap_type == "all" or gap_type == "verb":
                    masked_sentence, answer, options = get_verb_gap(
                        sentence_sanitized, mask_string
                    )
                    gap_data = format_gap_task(masked_sentence, answer, options, "verb")
                    if not gap_data is None:
                        dataset_with_gaps.append(gap_data)

    with open(output_file_path, "w", encoding="utf8") as f:
        json.dump(dataset_with_gaps, f)


if __name__ == "__main__":

    args = parse_args()
    main(args)
