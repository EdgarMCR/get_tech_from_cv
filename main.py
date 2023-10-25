
import re
from typing import List, Optional
from pathlib import Path
from dataclasses import dataclass

import pandas as pd

import script_utility as su


@dataclass
class Lang:
    name: str
    full_name: str
    year: str
    desc: str


def load_langs() -> List[Lang]:
    """ List of programming languages
    From https://www.scriptol.com/programming/list-programming-languages.php
    """
    langs = []
    path = Path(__file__).parent / 'lang_list.txt'
    with open(path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if lang := parse_line_into_lang(line):
            langs.append(lang)
    return langs


def load_langs_with_words_removed() -> List[Lang]:
    """ Remove programming languages that are also valid enlish words but are uncomen. """
    langs = load_langs()
    remove = ['T', 'S', 'K', 'B', 'ML', 'E']
    selected = [x for x in langs if x.name not in remove]
    return selected


def parse_line_into_lang(line: str) -> Optional[Lang]:
    if not line:
        return

    line = line.strip('\n')

    match = re.search(r'\. ', line)
    if not match:
        return

    full_name = line[:match.end()-2]
    line = line[match.end():].strip()
    if m2 := re.search(r', ', full_name):
        name = full_name[:m2.end()-2]
    else:
        name = full_name

    if match := re.match('\d{4}\.', line):
        year = match.group().strip('.')
        line = line[match.end():].strip()
    else:
        year = ''

    return Lang(name, full_name, year, line)




def load_kaggel_dataset():
    """ Resume  Dataset from
    https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset/
    """
    # Expect it to be in the same dir
    path = Path(__file__).parent / 'UpdatedResumeDataSet.csv'
    df = pd.read_csv(path)
    return df


def get_languages_in_text(text: str, langs: List[Lang]):
    found = []
    for lang in langs:
        contexts = []
        pattern = r'\b' + re.escape(lang.name) + r'(?!#)(?!\+)\b'
        for match in re.finditer(pattern, text):
            s, e = match.start() - 30, match.end() + 30
            if s < 0: s = 0
            if e > len(text): e = len(text)
            context = text[s:e]
            contexts.append(context)
        if contexts:
            found.append((lang, contexts))
    return found


def print_found_languages_with_context(text, langs):
    found = get_languages_in_text(text, langs)
    for lang, contexts in found:
        print("\nLanguage '{}'".format(lang.name))
        for context in contexts:
            print('-' * 30)
            print('\t"{}"'.format(context.replace('\n', '\n\t')))


@su.print_runtime
def main():
    df = load_kaggel_dataset()
    langs = load_langs_with_words_removed()

    for index, row in df.iterrows():
        text = row['Resume']
        print_found_languages_with_context(text, langs)

        if index > 2:
            break


if __name__ == '__main__':
    main()
