import enum
import Hint

def wordle_result(guess, true_word):
    true_word_list = list(true_word)

    result = ["b", "b", "b", "b", "b"] 
    for pos, guess_letter in enumerate(guess): 
        if guess_letter == true_word[pos]: 
            result[pos] = "g"
            true_word_list.remove(guess_letter)

    for pos, guess_letter in enumerate(guess): 
        if guess_letter in true_word_list and result[pos] != "g":
            result[pos] = "y"
            true_word_list.remove(guess_letter)

    return "".join(result)

def valid_guess_hard_mode(test_guess, guess, result):
    test_guess_letters = list(test_guess)
    for test_letter, letter, color in zip(test_guess, guess, result):
        if color == "g":
            if test_letter != letter: 
                return False
            test_guess_letters.remove(letter)
        elif color == "y":
            if letter not in test_guess_letters:
                return False
            test_guess_letters.remove(letter)
    return True
        
        
def wordle_metric(guess, true_word):
    guess = list(guess)
    true_word = list(true_word)
    greens = 0
    yellows = 0
    
    for true_letter, guess_letter in zip(true_word[:], guess[:]): 
        if guess_letter == true_letter: 
            greens += 1
            true_word.remove(guess_letter)
            guess.remove(guess_letter)

    for guess_letter in guess: 
        if guess_letter in true_word:
            yellows += 1
            true_word.remove(guess_letter)

    return greens, yellows

def num_greens(guess, true_word): 
    greens = 0
    for guess_letter, true_letter in zip(guess, true_word):
        if guess_letter == true_letter:
            greens += 1
    return greens

def num_yellows(guess, true_word): 
    def in_common(word, other):
        sum = 0
        for letter in word: 
            if letter in other:
                sum += 1
                other.remove(letter)
        return sum
    
    return in_common(guess, list(true_word)) - num_greens(guess, true_word)