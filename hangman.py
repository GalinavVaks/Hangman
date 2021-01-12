import hangman_ascii_art
import os 

def hangman():
    """ Play hangman. Requires the user enter a space-separated dictionary file,
        of which one is randomly chosen as the secret word
    """
    clear_screen()
    hangman_ascii_art.splash_screen()
    MAX_TRIES = 6
    words_path = input("Please enter the path to the words' file: ")
    secret_word = choose_word(words_path)
    print("You have %d attempts." % MAX_TRIES)
    old_letters_guessed = [] # Accumulates guessed letters
    failed_tries = 0 
    while failed_tries < MAX_TRIES:
        print(hangman_ascii_art.HANGMAN_PHOTOS[failed_tries])
        print(show_hidden_word(secret_word, old_letters_guessed))
        guessed_letter = input("Please enter a letter: ")
        while not try_update_letter_guessed(guessed_letter, old_letters_guessed):
            guessed_letter = input("Try again. Enter a letter: ")
        print(show_hidden_word(secret_word, old_letters_guessed))
        if check_win(secret_word, old_letters_guessed):
            print("WIN")
            break 
        elif guessed_letter not in secret_word:
            print(":(")
            failed_tries += 1

    if failed_tries >= MAX_TRIES: # The while loop ended without a win break
        print("LOSE. The word was %s." % secret_word)

def clear_screen(): 
    """ Clears the console screen
    """ 
    if os.name == 'nt': 
        os.system('cls') 
    else: 
        os.system('clear')             

def choose_word(file_path):
    """ Return a random word from the file
    """
    with open(file_path, "r") as input_file:
        words = input_file.read().split(" ")
    return words[randrange(len(words))]  
    
def show_hidden_word(secret_word, old_letters_guessed):
    """ Return a string showing what was guessed so far
    """
    return " ".join([i if i in old_letters_guessed else "_" for i in secret_word])

def check_valid_input(letter_guessed, old_letters_guessed):
    """ Return whether the input is a new, single letter 
    """
    if len(letter_guessed) != 1:
        return False
    if not(letter_guessed.isalpha()):
        return False
    if letter_guessed.lower() in list(map(str.lower, old_letters_guessed)):
        # Lower casing both to compare
        return False    
    return True
    
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """ Try to add new letter to old ones, return whether successful
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed += [letter_guessed.lower()]
        return True
    # Otherwise, inform of error and remind of guessed letters
    print("X")
    print(" -> ".join(sorted(old_letters_guessed)))
    return False
    
def check_win(secret_word, old_letters_guessed):
    """ Do all letters of secret_word appear in old_letters_guessed
    """
    return set(secret_word).issubset(set(old_letters_guessed))    
    
if __name__ == "__main__":
    hangman()