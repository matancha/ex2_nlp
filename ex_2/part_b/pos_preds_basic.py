import numpy as np
from collections import defaultdict, Counter
import math

word_maps = defaultdict(Counter)
pos_freq = Counter()
pos_distribution = None
word_maps_distribution = None

def populate_train_word_maps(file_path, limit=math.inf):
    with open(file_path, 'r', encoding='utf8') as file:
        for i, line in enumerate(file):
            if i > limit:
                break

            tag_pairs = line.split()
            for tag_pair in tag_pairs:
                token, pos = tag_pair.rsplit('/', 1)

                pos_freq[pos] += 1
                word_maps[token][pos] += 1

def normalize_counter(counter):
    total = sum(counter.values())
    return {k: v / total for k, v in counter.items()}


if __name__ == "__main__":
    workspaceFolder = "C://Study/bar_ilan/year_2024A/NLP/ex_2"
    data_dir = f'{workspaceFolder}/part_b/data-pos'
    train_file = "ass2-tagger-train"

    populate_train_word_maps(f'{data_dir}/{train_file}')
    pos_values = np.array(list(pos_freq.values()))
    pos_distribution = pos_values / pos_values.sum()

    word_maps_distribution = {key: normalize_counter(counter) for key, counter in word_maps.items()}

    dev_file = "ass2-tagger-dev-input" 
    test_file = "ass2-tagger-test-input" 
    with open(f'{data_dir}/{dev_file}', 'r', encoding='utf8') as file:
        with open(f'{data_dir}/ass2-tagger-dev-debug', 'w') as output:
            for i, line in enumerate(file):
                line_pos = []
                tokens = line.split()
                for token in tokens:
                    chosen_pos = None
                    if token in word_maps_distribution.keys():
                        chosen_pos = np.random.choice(list(word_maps_distribution[token].keys()), p=list(word_maps_distribution[token].values()))
                    else:
                        print(f'token {token} not in training')
                        chosen_pos = np.random.choice(list(pos_freq.keys()), p=pos_distribution)

                    line_pos.append(f'{token}/{chosen_pos}')

                output.write(' '.join(line_pos))
                output.write('\n')

    # for word in word_maps.keys():
    #     if len(word_maps[word]) > 1:
    #         print(word, word_maps[word])

    # print(pos_freq.keys(), pos_freq.values())