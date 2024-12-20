import numpy as np
from collections import defaultdict, Counter
import math
import re
from sklearn.metrics.pairwise import cosine_similarity
from transformers import RobertaTokenizerFast, RobertaModel
import torch

word_maps = defaultdict(Counter)
pos_freq = Counter()
pos_distribution = None
pos_transition_freq = defaultdict(Counter)
pos_transition_distribution = None
word_maps_distribution = None

num_regex = r'-?\d+(\,\d{3})*(\.\d+)?|(\d{1,2}:\d{2})'
CARDINAL_NUMBER_POS = 'CD'

tokenizer = RobertaTokenizerFast.from_pretrained("roberta-base")
model = RobertaModel.from_pretrained("roberta-base")

START_POS = 'START'
END_POS = 'END'

POS = ['START', 'END', 'IN', 'DT', 'NNP', 'CD', 'NN', '``', "''", 'POS', '(', 'VBN', 'NNS', 'VBP', ',', 'CC', ')', 'VBD', 'RB', 
'.', 'VBZ', 'NNPS', 'PRP', 'PRP$', 'TO', 'VB', 'JJ', 'MD', 'VBG', 'RBR', ':', 'WP', 'WDT', 'JJR', 'PDT', 'RBS', 'WRB', 'JJS', '$', 'RP', 'FW', 'EX', 'SYM', '#', 'LS', 'UH', 'WP$']

def calculate_word_embedding(sentence, target_word):
    inputs = tokenizer(sentence, return_tensors='pt', return_offsets_mapping=True)
    word_indices = [idx for idx, (start, end) in enumerate(inputs['offset_mapping'][0].tolist()) if sentence[start:end] == target_word]
    inputs = tokenizer(sentence, return_tensors='pt')

    with torch.no_grad():
        outputs = model(**inputs)

    hidden_states = outputs.last_hidden_state
    word_embeddings = hidden_states[0, word_indices, :]

    if word_embeddings.shape[0] > 1:
        word_embedding = word_embeddings.mean(dim=0)
    else:
        word_embedding = word_embeddings.squeeze(0)

    return word_embedding

def get_tokenized_words(sentence):
    inputs = tokenizer(sentence, return_tensors='pt', return_offsets_mapping=True)
    words = [sentence[start:end] for (start, end) in inputs['offset_mapping'][0].tolist()]
    return words

def populate_train_word_maps(file_path, limit=math.inf):
    with open(file_path, 'r', encoding='utf8') as file:
        for i, line in enumerate(file):
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

def normalize_counter(counter):
    total = sum(counter.values())
    return {k: v / total for k, v in counter.items()}


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
                    # elif token in vectorizer.index_to_key and any(item in word_maps.keys() for item in most_similar(token)):
                    #     hits += 1
                    #     most_similar_word = list(filter(lambda x: x in word_maps.keys(), most_similar(token)))[0]
                    #     print(f'most similar to {token} is {most_similar_word}')
                    #     transition_values = np.array([pos_transition_distribution[prev_tag][pos] for pos in word_maps_distribution[most_similar_word].keys()], dtype=float)
                    #     adjusted_values = np.array(list(word_maps_distribution[most_similar_word].values()), dtype=float) * transition_values
                    #     chosen_pos = np.random.choice(list(word_maps_distribution[most_similar_word].keys()), p=adjusted_values / adjusted_values.sum())
                    # elif token.lower() in vectorizer.index_to_key and any(item in word_maps.keys() for item in most_similar(token.lower())):
                    #     hits += 1
                    #     most_similar_word = list(filter(lambda x: x in word_maps.keys(), most_similar(token.lower())))[0]
                    #     print(f'most similar to lowercase {token} is {most_similar_word}')
                    #     transition_values = np.array([pos_transition_distribution[prev_tag][pos] for pos in word_maps_distribution[most_similar_word].keys()], dtype=float)
                    #     adjusted_values = np.array(list(word_maps_distribution[most_similar_word].values()), dtype=float) * transition_values
                    #     chosen_pos = np.random.choice(list(word_maps_distribution[most_similar_word].keys()), p=adjusted_values / adjusted_values.sum())
                    elif True:
                        pass
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