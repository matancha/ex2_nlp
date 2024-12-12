if __name__ == "__main__":
    workspaceFolder = "C://Study/bar_ilan/year_2024A/NLP/ex_2"
    data_dir = f'{workspaceFolder}/part_b/data-pos'

    gold_standard_file = 'ass2-tagger-dev'
    output_file = 'ass2-tagger-dev-debug'

    tokens_predicted = 0
    tokens_wrong = 0
    with open(f'{data_dir}/{gold_standard_file}', 'r') as gold_standard:
        with open(f'{data_dir}/{output_file}', 'r') as debug:
            for debug_line, gold_standard_line in zip(debug, gold_standard):
                tag_pairs_debug_line, tag_pairs_gold_standard_line = debug_line.split(), gold_standard_line.split()
                for tag_pair_debug_line, tag_pairs_gold_standard_line in zip(tag_pairs_debug_line, tag_pairs_gold_standard_line):
                    tokens_predicted += 1
                    token_debug_line, pos_debug_line = tag_pair_debug_line.rsplit('/', 1)
                    token_gold_standard_line, pos_gold_standard_line = tag_pairs_gold_standard_line.rsplit('/', 1)
                    if pos_debug_line != pos_gold_standard_line:
                        tokens_wrong += 1
                        if token_debug_line != token_gold_standard_line:
                            raise Exception
                        print(token_debug_line, pos_debug_line, pos_gold_standard_line)

            print(f'acc is {(tokens_predicted-tokens_wrong) / tokens_predicted}')

                