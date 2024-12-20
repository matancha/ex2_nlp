import numpy as np
from collections import defaultdict, Counter
import math
import gensim.downloader as dl
import re
from sklearn.metrics.pairwise import cosine_similarity
import time

word_maps = defaultdict(Counter)
pos_freq = Counter()
pos_distribution = None
pos_transition_freq = defaultdict(Counter)
pos_transition_distribution = None
word_maps_distribution = None

pos_vectors = defaultdict(list)

num_regex = r'-?\d+(\,\d{3})*(\.\d+)?|(\d{1,2}:\d{2})'
CARDINAL_NUMBER_POS = 'CD'

vectorizer = dl.load("glove-wiki-gigaword-200")
# seen_word_vecs = {}

START_POS = 'START'
END_POS = 'END'

POS = ['START', 'END', 'IN', 'DT', 'NNP', 'CD', 'NN', '``', "''", 'POS', '(', 'VBN', 'NNS', 'VBP', ',', 'CC', ')', 'VBD', 'RB', 
'.', 'VBZ', 'NNPS', 'PRP', 'PRP$', 'TO', 'VB', 'JJ', 'MD', 'VBG', 'RBR', ':', 'WP', 'WDT', 'JJR', 'PDT', 'RBS', 'WRB', 'JJS', '$', 'RP', 'FW', 'EX', 'SYM', '#', 'LS', 'UH', 'WP$']

def most_similar(word):
    return list(map(lambda x: x[0], vectorizer.most_similar(word)))

def populate_train_word_maps(file_path, limit=math.inf):
    start_time = time.time()
    with open(file_path, 'r', encoding='utf8') as file:
        for i, line in enumerate(file):
            if (i % 1000 == 0):
                print (f'=== {i}, {time.time() - start_time:.3f} sec ===')

            if i > limit:
                break

            tag_pairs = line.split()
            previous_pos = START_POS
            for tag_pair in tag_pairs:
                token, pos = tag_pair.rsplit('/', 1)
                # if re.fullmatch(num_regex, token):
                #     continue

                pos_freq[pos] += 1
                word_maps[token][pos] += 1
                pos_transition_freq[previous_pos][pos] += 1
                previous_pos = pos

            pos_transition_freq[previous_pos][END_POS] += 1

                # if token in vectorizer.index_to_key:
                #     seen_word_vecs[token] = vectorizer[token]

def normalize_counter(counter):
    total = sum(counter.values())
    return {k: v / total for k, v in counter.items()}


# try_and_lower(token, lambda x: x in word_maps_distribution.keys(), lambda y: np.random.choice(list(word_maps_distribution[y].keys()), p=list(word_maps_distribution[y].values())))
# def try_and_lower(token, cond, then):
#     # elif token in word_maps_distribution.keys():
#     #                     chosen_pos = np.random.choice(list(word_maps_distribution[token].keys()), p=list(word_maps_distribution[token].values()))
#     if cond(token): return then(token)
#     if cond(token.lower()): return then(token.lower())
#     return ''


if __name__ == "__main__":
    workspaceFolder = "C://Study/bar_ilan/year_2024A/NLP/ex_2"
    data_dir = f'{workspaceFolder}/part_b/data-pos'
    train_file = "ass2-tagger-train"

    for pos in POS:
        pos_transition_freq[START_POS][pos] = 1
        pos_transition_freq[pos][END_POS] = 1
        for next_pos in POS:
            pos_transition_freq[pos][next_pos] = 1

    populate_train_word_maps(f'{data_dir}/{train_file}')
    pos_values = np.array(list(pos_freq.values()))
    pos_distribution = pos_values / pos_values.sum()

    word_maps_distribution = {key: normalize_counter(counter) for key, counter in word_maps.items()}
    pos_transition_distribution = {key: normalize_counter(counter) for key, counter in pos_transition_freq.items()}

    dev_file = "ass2-tagger-dev-input" 
    test_file = "ass2-tagger-test-input" 
    hits = 0
    with open(f'{data_dir}/{dev_file}', 'r', encoding='utf8') as file:
        with open(f'{data_dir}/ass2-tagger-dev-debug', 'w') as output:
            for i, line in enumerate(file):
                line_pos = []
                prev_tag = START_POS
                tokens = line.split()
                for token in tokens:
                    chosen_pos = None
                    if re.fullmatch(num_regex, token):
                        chosen_pos = CARDINAL_NUMBER_POS
                    elif token in word_maps_distribution.keys() or token.lower() in word_maps_distribution.keys():
                        matched_token = token if token in word_maps_distribution.keys() else token.lower()
                        transition_values = np.array([pos_transition_distribution[prev_tag][pos] for pos in word_maps_distribution[matched_token].keys()], dtype=float)
                        adjusted_values = np.array(list(word_maps_distribution[matched_token].values()), dtype=float) * transition_values
                        chosen_pos = np.random.choice(list(word_maps_distribution[matched_token].keys()), p=adjusted_values / adjusted_values.sum())
                        # chosen_pos = list(word_maps_distribution[matched_token].keys())[np.argmax(adjusted_values)]
                    elif token in vectorizer.index_to_key and any(item in word_maps.keys() for item in most_similar(token)):
                        hits += 1
                        # print(token, list(filter(lambda x: x in word_maps.keys(), most_similar(token.lower()))))
                        all_words = list(filter(lambda x: x in word_maps.keys(), most_similar(token)))
                        print([word_maps_distribution[word] for word in all_words])
                        most_similar_word = list(filter(lambda x: x in word_maps.keys(), most_similar(token)))[0]
                        print(f'most similar to {token} is {most_similar_word}')
                        transition_values = np.array([pos_transition_distribution[prev_tag][pos] for pos in word_maps_distribution[most_similar_word].keys()], dtype=float)
                        adjusted_values = np.array(list(word_maps_distribution[most_similar_word].values()), dtype=float) * transition_values
                        chosen_pos = np.random.choice(list(word_maps_distribution[most_similar_word].keys()), p=adjusted_values / adjusted_values.sum())
                        # chosen_pos = np.random.choice(list(word_maps_distribution[most_similar_word].keys()), p=list(word_maps_distribution[most_similar_word].values()))
                    elif token.lower() in vectorizer.index_to_key and any(item in word_maps.keys() for item in most_similar(token.lower())):
                        hits += 1
                        # print(token, list(filter(lambda x: x in word_maps.keys(), most_similar(token.lower()))))
                        most_similar_word = list(filter(lambda x: x in word_maps.keys(), most_similar(token.lower())))[0]
                        print(f'most similar to lowercase {token} is {most_similar_word}')
                        transition_values = np.array([pos_transition_distribution[prev_tag][pos] for pos in word_maps_distribution[most_similar_word].keys()], dtype=float)
                        adjusted_values = np.array(list(word_maps_distribution[most_similar_word].values()), dtype=float) * transition_values
                        chosen_pos = np.random.choice(list(word_maps_distribution[most_similar_word].keys()), p=adjusted_values / adjusted_values.sum())
                        # chosen_pos = np.random.choice(list(word_maps_distribution[most_similar_word].keys()), p=list(word_maps_distribution[most_similar_word].values()))
                    elif token.istitle():
                        if token[-1] == 's':
                            chosen_pos = 'NNPS'
                        else:
                            chosen_pos = 'NNP'
                    else:
                        # print(f'token {token} not in training')
                        transition_values = np.array([pos_transition_distribution[prev_tag][pos] for pos in pos_freq.keys()], dtype=float)
                        adjusted_values = np.array(list(pos_distribution), dtype=float) * transition_values
                        chosen_pos = np.random.choice(list(pos_freq.keys()), p=transition_values / transition_values.sum())

                    line_pos.append(f'{token}/{chosen_pos}')
                    prev_tag = chosen_pos

                output.write(' '.join(line_pos))
                output.write('\n')

    print(f'word match hits are {hits}')