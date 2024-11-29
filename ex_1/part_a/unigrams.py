def print_counts(filename, is_hebrew=False):
    """
    Print counts dictionary line by line in format "token:num"
    Args:
        counts_dict: Dictionary containing token counts
        is_hebrew: Boolean indicating if the text is Hebrew (for right-to-left display)
    """
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            token, count = line.split(':')
            count = count.rstrip()
            print(f'{token}:{count}')

configs = {
    "1": {
        "filename": "english_counts.txt",
    },
    "2": {
        "filename": "hebrew_counts.txt",
    },
}

if __name__ == '__main__':
    default_path = r"C:\Study\bar_ilan\year_2024A\NLP\ex_1"
    
    print("Choose language to analyze:")
    print("1. english")
    print("2. hebrew")
    
    choice = input("Enter 1 or 2: ")

    config = configs[choice]
    full_path = f"{default_path}\\{config['filename']}"
    
    print("English counts:")
    print_counts(f"{default_path}\\{config['filename']}")