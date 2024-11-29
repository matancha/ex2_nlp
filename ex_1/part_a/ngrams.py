from collections import defaultdict, Counter
from bidi.algorithm import get_display
import string
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import time
import sqlite3

n_english = 84_734_015
n_hebrew = 63_616_482

WINDOW_SIZE = 10

conn = sqlite3.connect("ngrams.db")
cursor = conn.cursor()

token_to_int = {}
int_to_token = {}

def load_counts(counts_filename):
    current_index = 0
    with open(counts_filename, 'r', encoding='utf-8') as file:
        for line in file:
            token, count = line.split(':')
            token = token[1:len(token)-1]
            count = int(count.rstrip())
            if count < WINDOW_SIZE:
                break
            
            if token not in token_to_int:
                token_to_int[token] = current_index
                int_to_token[current_index] = token
                current_index += 1

# ngram_to_int = {}
# int_to_ngram = {}

def process_line(text):
    words = [word.strip(string.punctuation).lower() 
                for word in str(text).split() 
                if word.strip(string.punctuation)]
    
    return words

def count_ngrams(filename):
    start_time = time.time()
    ngrams_count = Counter()
    # current_index = 0

    with open(filename, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if (i % 100000 == 0):
                print (f'=== {i}, {time.time() - start_time:.3f} sec ===')
            # if i == 100000:
            #     return ngrams_count
            words = [word.lower().strip(string.punctuation) 
                    for word in line.split() 
                    if word.strip(string.punctuation)]
            
            if len(words) >= WINDOW_SIZE:
                words_array = np.array(words, dtype=object)
                windows = sliding_window_view(words_array, WINDOW_SIZE)
                
                for window in windows:
                    tokened_window = list(map(lambda t: str(token_to_int.get(t, '<unk>')), window))
                    if '<unk>' not in tokened_window:
                        ngrams_count[','.join(tokened_window)] += 1
                    # if ngram not in ngram_to_int:
                    #     ngram_to_int[ngram] = current_index
                    #     int_to_ngram[current_index] = ngram
                    #     current_index += 1

                    # ngram_int = ngram_to_int[ngram]
                    # ngrams_count[ngram_int] += 1

    return ngrams_count

def write_counts_to_file(result, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as file:
        i = 1
        for ngram, count in result.most_common():
            if i > 100:
                return
            tokens = list(map(lambda idx: int_to_token[int(idx)], ngram.split(',')))
            file.write(f"{','.join(tokens)}: {count}\n")
            i += 1

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
    # Default path
    default_path = r"C:\Study\bar_ilan\year_2024A\NLP\ex_1"
    
    # Let user choose the file
    print("Choose language to analyze:")
    print("1. english")
    print("2. hebrew")
    
    choice = input("Enter 1 or 2: ")

    config = configs[choice]
    # Combine default path with filename
    full_path = f"{default_path}\\{config['filename']}"
    
    # Create output filename based on input file
    output_filename = f"{default_path}\\{config['filename'].split('.')[0]}_ngrams_{WINDOW_SIZE}.txt"
    # Get and display word counts
    try:
        load_counts(f"{default_path}\\{config['counts_filename']}")
        result = count_ngrams(full_path) 
        # print(f'Total words with repeats: {total_words_with_repeats}')     
        # print(f'Total unique words: {unique_words_count}')
        write_counts_to_file(result, output_filename)
        
    except FileNotFoundError:
        print(f"Error: Could not find file at {full_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()