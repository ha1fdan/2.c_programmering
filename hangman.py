import random
import os

words = ["motorvej", "jernbane", "vindmolle", "frugtbar", "isterning", "kryptering", "legoklods", "fodboldhold", "tidsrejse"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_hangman(attempts_left):
    """Draw hangman based on remaining attempts"""
    stages = [
        # 0 attempts left
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        Game Over!
        """,
        # 1 attempt left
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     /
           -
        """,
        # 2 attempts left
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |
           -
        """,
        # 3 attempts left
        """
           --------
           |      |
           |      O
           |     \\|
           |      |
           |
           -
        """,
        # 4 attempts left
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |
           -
        """,
        # 5 attempts left
        """
           --------
           |      |
           |      O
           |
           |
           |
           -
        """,
        # 6 attempts left
        """
           --------
           |      |
           |
           |
           |
           |
           -
        """
    ]
    print(stages[6 - attempts_left])

def display_header():
    """Display game header"""
    print("""
    ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓██████████████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░  
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                                 
    """)
    print("=" * 60)
    print("Welcome to Hangman! Guess the Danish word letter by letter.")
    print("=" * 60)

def display_word_progress(word, guessed_letters):
    """Display the current progress of the word"""
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()

def play_hangman():
    """Main game function"""
    word = random.choice(words)
    letters_in_word = set(word)
    guessed_letters = set()
    attempts = 6
    
    clear_screen()
    display_header()
    
    while attempts > 0 and not letters_in_word.issubset(guessed_letters):
        print()
        draw_hangman(attempts)
        print(f"\nAttempts remaining: {attempts}")
        print(f"Word: {display_word_progress(word, guessed_letters)}")
        print(f"Word length: {len(word)} letters")
        
        if guessed_letters:
            correct_guesses = sorted([letter for letter in guessed_letters if letter in letters_in_word])
            wrong_guesses = sorted([letter for letter in guessed_letters if letter not in letters_in_word])
            
            if correct_guesses:
                print(f"Correct guesses: {', '.join(correct_guesses)}")
            if wrong_guesses:
                print(f"Wrong guesses: {', '.join(wrong_guesses)}")
        
        print("-" * 40)
        
        # Get user input
        while True:
            guess = input("Guess a letter: ").lower().strip()
            
            if len(guess) != 1:
                print("Please enter exactly one letter.")
                continue
                
            if not guess.isalpha():
                print("Please enter a valid letter (a-z).")
                continue
                
            if guess in guessed_letters:
                print("You already guessed that letter. Try again.")
                continue
                
            break
        
        guessed_letters.add(guess)
        
        if guess in letters_in_word:
            print(f"✓ Good guess! '{guess}' is in the word.")
            # Check if word is complete
            if letters_in_word.issubset(guessed_letters):
                clear_screen()
                display_header()
                print("\n🎉 CONGRATULATIONS! 🎉")
                print(f"You've successfully guessed the word: {word.upper()}")
                print(f"You had {attempts} attempts remaining.")
                break
        else:
            attempts -= 1
            print(f"✗ Sorry! '{guess}' is not in the word.")
            if attempts > 0:
                print(f"You have {attempts} attempts left.")
    
    # Game over - player lost
    if attempts == 0:
        clear_screen()
        display_header()
        draw_hangman(0)
        print(f"\n💀 GAME OVER! 💀")
        print(f"The word was: {word.upper()}")
    
    print("\nThanks for playing Hangman!")
    
    # Ask to play again
    while True:
        play_again = input("\nWould you like to play again? (y/n): ").lower().strip()
        if play_again in ['y', 'yes']:
            play_hangman()
            break
        elif play_again in ['n', 'no']:
            print("Goodbye! Hope you enjoyed the game!")
            break
        else:
            print("Please enter 'y' for yes or 'n' for no.")

# Start the game
if __name__ == "__main__":
    play_hangman()