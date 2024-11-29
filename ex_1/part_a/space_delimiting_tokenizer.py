from collections import defaultdict, Counter
from bidi.algorithm import get_display
import string

n_english = 84_734_015
n_hebrew = 63_616_482

def count_words(filename, n_tokens):
    # Using Counter for word counting
    word_count = Counter()
    
    with open(filename, 'r', encoding='utf-8') as file:
        total_words_with_repeats = 0
        for line in file:
            # Split on whitespace first
            words = line.split()
            
            # Clean words by only removing punctuation at start/end
            cleaned_words = []
            for word in words:
                # Strip punctuation only from start and end of word
                word = word.strip(string.punctuation)
                if word:  # if anything remains after stripping
                    cleaned_words.append(word.lower())
            
            # Update counter with all words at once
            word_count.update(cleaned_words)
            total_words_with_repeats += len(cleaned_words)
            if total_words_with_repeats >= n_tokens:
                break

    return word_count, total_words_with_repeats, len(word_count)

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
    default_path = r"C:\Study\Bar Ilan\Year 1\NLP\Ex 1"
    
    # Let user choose the file
    print("Choose language to analyze:")
    print("1. english")
    print("2. hebrew")
    
    choice = input("Enter 1 or 2: ")

    config = configs[choice]
    # Combine default path with filename
    full_path = f"{default_path}\\{config['filename']}"
    
    # Create output filename based on input file
    output_filename = f"{default_path}\\{config['filename'].split('.')[0]}_counts.txt"
    output_filename_half = f"{default_path}\\{config['filename'].split('.')[0]}_counts_half.txt"
    # Get and display word counts
    try:
        # result, total_words_with_repeats, unique_words_count = count_words(full_path, n_tokens=config['n_tokens']) 
        # print(f'Total words with repeats: {total_words_with_repeats}')     
        # print(f'Total unique words: {unique_words_count}')
        # write_counts_to_file(result, output_filename)

        result, total_words_with_repeats_half , unique_words_count_half = count_words(full_path, n_tokens=config['n_tokens']/2)     
        print(f'Total words with repeats (n/2): {total_words_with_repeats_half}')     
        print(f'Total unique words (n/2): {unique_words_count_half}')    
        write_counts_to_file(result, output_filename_half)
        
    except FileNotFoundError:
        print(f"Error: Could not find file at {full_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()