import string
import time
from collections import defaultdict, Counter
import math
from copy import deepcopy
import re

SUBTOKEN_END_SYMBOL = '§'

nikkud_pattern = r"[\u0591-\u05C7]"
right_to_left_pattern = r"[\u200E-\u200F]"
hebrew_chars_to_remove_pattern = f"{nikkud_pattern}|{right_to_left_pattern}"

def count_words(filename):
    word_count = Counter()
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.split()
            
            cleaned_words = []
            for word in words:
                word = re.sub(hebrew_chars_to_remove_pattern, "", word)
                word = word.strip(string.punctuation)
                if word: 
                    cleaned_words.append(" ".join(word.lower() + SUBTOKEN_END_SYMBOL))
            
            word_count.update(cleaned_words)

    return word_count

# def load_counts(counts_filename):
#     with open(counts_filename, 'r', encoding='utf-8') as file:
#         for line in file:
#             token, count = line.split(': ')
#             token = token[1:len(token)-1]
#             count = int(count.rstrip())

# def train_bpe(filename, N):
#     start_time = time.time()
#     # token_counts, a, b = count_words(filename)
#     token_counts = Counter({'the': 15, 'world': 5, 'is': 5, 'a': 10, 'joke': 25})

#     vocabulary = set('the' + 'world' + 'is' + 'a' + 'joke')
#     pair_counts = defaultdict(int)
#     for token, freq in token_counts.items():
#         for i in range(len(token) - 1):
#             pair = (token[i], token[i+1])
#             pair_counts[pair] += freq

#     while len(vocabulary) < N:
#         if not pair_counts:
#             break
        
#         most_frequent_pair = max(pair_counts, key=pair_counts.get)
#         if pair_counts[most_frequent_pair] == 0:
#             break
        
#         # Merge the most frequent pair
#         new_token = ''.join(most_frequent_pair)
#         vocabulary.add(new_token)

#         # Update tokens and pair counts
#         new_token_counts = Counter()
#         updated_pairs = defaultdict(int)
        
#         for token, freq in token_counts.items():
#             new_tokenized = []
#             i = 0
#             while i < len(token):
#                 # If a pair match is found, replace it
#                 if i < len(token) - 1 and (token[i], token[i+1]) == most_frequent_pair:
#                     new_tokenized.append(new_token)
#                     i += 2  # Skip the merged pair
#                 else:
#                     new_tokenized.append(token[i])
#                     i += 1

#             new_tokenized = ''.join(new_tokenized)
#             new_token_counts[new_tokenized] += freq

#             for i in range(len(new_tokenized) - 1):
#                 updated_pairs[(new_tokenized[i], new_tokenized[i+1])] += freq

#         token_counts = new_token_counts
#         pair_counts = updated_pairs

#     return sorted(vocabulary)

def train_bpe(filename, N):
    start_time = time.time()
    # tokens = {'the': 15, 'world': 5, 'is': 5, 'a': 10, 'joke': 25, 'jojo': 5}
    # token_counts = Counter()
    
    # for token in tokens:
    #     subtokenized = ' '.join(token + SUBTOKEN_END_SYMBOL)
    #     token_counts[subtokenized] = tokens[token]

    token_counts = count_words(filename)
    vocabulary = []
    epoch = 1

    transitions = Counter()
    for token, count in token_counts.items():
        token = token.split(' ')
        for i in range(len(token)-1):
            subtoken = token[i] + 'SEP' + token[i+1]
            transitions[subtoken] += count

    while len(vocabulary) < N:
        # TODO: not reset transition every epoch (V)
        merged_subtoken, count = transitions.most_common(1)[0]
        non_delimited = merged_subtoken.split('SEP')
        vocabulary.append(non_delimited[0] + non_delimited[1])
        print(non_delimited[0] + non_delimited[1])

        # updated_token_counts = Counter()
        # TODO: keep track of tokens that need to be changed
        token_counts_copy = deepcopy(token_counts)
        for token, count in token_counts_copy.items():
            if f'{non_delimited[0]} {non_delimited[1]}' in token:
                del token_counts[token]
            else:
                continue
            
            list_token = token.split(' ')
            list_new_token = []
            i = 0
            while i < len(list_token):
                if list_token[i:i+2] == non_delimited:
                    list_new_token.append(non_delimited[0] + non_delimited[1])
                    i += 2
                else:
                    list_new_token.append(list_token[i])
                    i += 1
                    
            for i in range(len(list_new_token)):
                if list_new_token[i] == non_delimited[0] + non_delimited[1]:
                    if i > 0 and list_new_token[i-1] != list_new_token[i]:
                        transitions[list_new_token[i-1] + 'SEP' + list_new_token[i]] += count
                    if i < len(list_new_token)-1:
                        # print(list_new_token[i] + 'SEP' + list_new_token[i+1])
                        if list_new_token[i] == list_new_token[i+1]:
                            # print('removed from', list_new_token[i][-1] + 'SEP' + list_new_token[i][0])
                            transitions[list_new_token[i][-1] + 'SEP' + list_new_token[i][0]] -= count
                        transitions[list_new_token[i] + 'SEP' + list_new_token[i+1]] += count
            del transitions[non_delimited[0] + 'SEP' + non_delimited[1]]

            # Optimization: filter out tokens that can't be merged anymore
            if len(list_new_token) > 1:
                token_counts[" ".join(list_new_token)] += count

        # token_counts = updated_token_counts

        print (f'=== {epoch}, {time.time() - start_time:.3f} sec ===')
        epoch += 1
        # print(transitions)
        print(token_counts.most_common(10))

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

def main():
    # N = 30_000
    N = 1000
    default_path = r"C:\Study\bar_ilan\year_2024A\NLP\ex_1"
    
    print("Choose language to analyze:")
    print("1. english")
    print("2. hebrew")
    
    choice = input("Enter 1 or 2: ")

    config = configs[choice]
    full_path = f"{default_path}\\{config['filename']}"
    
    vocabulary = train_bpe(full_path, N)
    print(vocabulary)

if __name__ == "__main__":
    main()