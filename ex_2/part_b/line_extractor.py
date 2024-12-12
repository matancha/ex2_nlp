import sys

pos_freq =({'NN': 132935, 'IN': 107862, 'NNP': 91466, 'DT': 81832, 'JJ': 61217,
            'NNS': 59856, ',': 48727, '.': 39478, 'CD': 36568, 'RB': 30970, 'VBD': 29889,
            'VB': 26438, 'CC': 23959, 'VBZ': 21672, 'VBN': 20024, 'PRP': 17436, 'VBG': 14846,
            'TO': 13049, 'VBP': 12491, 'MD': 9803, 'POS': 8701, 'PRP$': 8407, '$': 7372,
            '``': 7092, "''": 6919, ':': 4772, 'WDT': 4294, 'JJR': 3238, 'NNPS': 2673, 'RP': 2662,
            'WP': 2363, 'WRB': 2143, 'JJS': 1947, 'RBR': 1768, ')': 1376, '(': 1366, 'EX': 863, 'RBS': 451, 'PDT': 368, 'FW': 234,
            'WP$': 168, '#': 142, 'UH': 97, 'SYM': 58, 'LS': 36})

def extract_lines_with_word(file_path, word, pos=pos_freq.keys()):
    with open(file_path, 'r', encoding='utf8') as file:
        for line in file:
            should_print = False
            tag_pairs = line.split()
            for tag_pair in tag_pairs:
                token, actual_pos = tag_pair.rsplit('/', 1)

                if token == word and actual_pos in pos:
                    should_print = True

            if should_print:
                print(line)

def normalize_counter(counter):
    total = sum(counter.values())
    return {k: v / total for k, v in counter.items()}


if __name__ == "__main__":
    input_pos = None
    input_word = sys.argv[1]
    if len(sys.argv) > 2:
        input_pos = sys.argv[2]

    workspaceFolder = "C://Study/bar_ilan/year_2024A/NLP/ex_2"
    data_dir = f'{workspaceFolder}/part_b/data-pos'
    train_file = "ass2-tagger-train"

    if input_pos:
        extract_lines_with_word(f'{data_dir}/{train_file}', input_word, input_pos)
    else:
        extract_lines_with_word(f'{data_dir}/{train_file}', input_word)