from collections import defaultdict, Counter
from bidi.algorithm import get_display
import string

n_english = 84_734_015
n_hebrew = 63_616_482

WINDOW_SIZE = 5

def process_line(text):
    words = [word.strip(string.punctuation).lower() 
                for word in str(text).split() 
                if word.strip(string.punctuation)]
    
    return words

def count_ngrams(filename):
    ngrams = []
    ngrams_count = Counter()

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.split()
            # print(words)
            
            cleaned_words = []
            for word in words:
                word = word.strip(string.punctuation)
                if word:
                    cleaned_words.append(word.lower())

            ngrams = []
            if len(cleaned_words) > WINDOW_SIZE:
                for i in range(len(cleaned_words)-WINDOW_SIZE):
                    ngram = cleaned_words[i:i+WINDOW_SIZE]
                    ngrams.append(','.join(ngram))
            
            ngrams_count.update(ngrams)

    return ngrams_count
    
    # with open(filename, 'r', encoding='utf-8') as file:
    #     lines = file.readlines()

    # df = pd.DataFrame({'text': [line.strip() for line in lines if line.strip()]})

    # vectorized_function = np.vectorize(process_line)
    # df['cleaned'] = vectorized_function(df['text'].values)
    # print(df.head(1))

    # return word_count, total_words_with_repeats, len(word_count)

def write_counts_to_file(result, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as file:
        for word, count in result.most_common():
            display_word = get_display(word)
            file.write(f"'{display_word}': {count}\n")

configs = {
    "1": {
        "filename": "english.txt",
        "n_tokens": n_english
    },
    "2": {
        "filename": "hebrew.txt",
        "n_tokens": n_hebrew
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
    output_filename = f"{default_path}\\{config['filename'].split('.')[0]}_ngrams.txt"
    # Get and display word counts
    try:
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