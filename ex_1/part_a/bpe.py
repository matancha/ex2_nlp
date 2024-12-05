import string
import time
from collections import Counter
from bidi.algorithm import get_display
from functools import cmp_to_key
import math
from copy import deepcopy
import re

SUBTOKEN_END_SYMBOL = '§'

replacements = {
    'ך': 'כ',
    'ם': 'מ',
    'ן': 'נ',
    'ף': 'פ',
    'ץ': 'צ'
}

translation_table = str.maketrans(replacements)

nikkud_pattern = r"[\u0591-\u05C7]"
right_to_left_pattern = r"[\u200E-\u200F]"
hebrew_chars_to_remove_pattern = f"{nikkud_pattern}|{right_to_left_pattern}"
separator = 'SEP'

def count_words(filename):
    word_count = Counter()
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.split()
            
            cleaned_words = []
            for word in words:
                word = re.sub(hebrew_chars_to_remove_pattern, "", word)
                word = word.strip(string.punctuation)
                word = word.translate(translation_table)
                if word: 
                    cleaned_words.append(" ".join(word.lower() + SUBTOKEN_END_SYMBOL))
            
            word_count.update(cleaned_words)

    return word_count

def train_bpe(filename, N):
    # start_time = time.time()
    token_counts = count_words(filename)
    vocabulary = []
    # epoch = 1

    transitions = Counter()
    for token, count in token_counts.items():
        token = token.split(' ')
        for merged_token_idx in range(len(token)-1):
            subtoken = token[merged_token_idx] + separator + token[merged_token_idx+1]
            transitions[subtoken] += count

    while len(vocabulary) < N:
        merged_subtoken, count = transitions.most_common(1)[0]
        non_delimited = merged_subtoken.split(separator)
        new_voc = non_delimited[0] + non_delimited[1]
        vocabulary.append(new_voc)
        # print(new_voc)

        for token, count in deepcopy(token_counts).items():
            if f'{non_delimited[0]} {non_delimited[1]}' in token:
                del token_counts[token]
            else:
                # Optimization: skip dealing with tokens that do not contain the merged transition
                continue
            
            sep_token = token.split(' ')
            sep_new_token = []
            unmerged_token_idx = 0
            while unmerged_token_idx < len(sep_token):
                if sep_token[unmerged_token_idx:unmerged_token_idx+2] == non_delimited:
                    sep_new_token.append(new_voc)
                    unmerged_token_idx += 2
                else:
                    sep_new_token.append(sep_token[merged_token_idx])
                    unmerged_token_idx += 1
                    
            # Optimization: update transitions dict for diffs and not build it every epoch
            for merged_token_idx in range(len(sep_new_token)):
                if sep_new_token[merged_token_idx] == new_voc:
                    if merged_token_idx > 0 and sep_new_token[merged_token_idx-1] != sep_new_token[merged_token_idx]:
                        transitions[sep_new_token[merged_token_idx-1] + separator + sep_new_token[merged_token_idx]] += count
                    if merged_token_idx < len(sep_new_token)-1:
                        if sep_new_token[merged_token_idx] == sep_new_token[merged_token_idx+1]:
                            transitions[sep_new_token[merged_token_idx][-1] + separator + sep_new_token[merged_token_idx][0]] -= count
                        transitions[sep_new_token[merged_token_idx] + separator + sep_new_token[merged_token_idx+1]] += count
            del transitions[non_delimited[0] + separator + non_delimited[1]]

            # Optimization: filter out tokens that can't be merged anymore
            if len(sep_new_token) > 1:
                token_counts[" ".join(sep_new_token)] = count

        # print (f'=== {epoch}, {time.time() - start_time:.3f} sec ===')
        # epoch += 1
        # print(token_counts.most_common(10))

    return vocabulary

configs = {
    "1": {
        "filename": "english.txt",
        "counts_filename": "english_counts.txt"
    },
    "2": {
        "filename": "hebrew.txt",
        "counts_filename": "hebrew_counts.txt"
    },
}

def custom_comparator(word1, word2):
    for char1, char2 in zip(word1, word2):
        if char1 < char2:
            return -1
        elif char1 > char2:
            return 1
    return -1 if len(word1) > len(word2) else 1 if len(word1) < len(word2) else 0

def write_to_file(result, output_filename):
    with open(output_filename, 'a', encoding='utf-8') as file:
        for word in sorted(result, key=cmp_to_key(custom_comparator)):
            display_word = get_display(word)
            file.write(f"{display_word} ")

def main():
    N = 30_000
    # N = 100
    default_path = r"C:\Study\bar_ilan\year_2024A\NLP\ex_1"
    
    print("Choose language to analyze:")
    print("1. english")
    print("2. hebrew")
    
    choice = input("Enter 1 or 2: ")

    config = configs[choice]
    full_path = f"{default_path}\\{config['filename']}"
    
    vocabulary = train_bpe(full_path, N)
    write_to_file(vocabulary, f'vocabulary_{N}_{config['filename']}')

if __name__ == "__main__":
    main()