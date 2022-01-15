from Words import *
import sys, re

print("Welcome to the wordle solver!")

def user_input():
    user_input = input("> ").strip().lower()
    print()
    if (user_input == "exit"):
        sys.exit()
    return user_input

def guess_input(): 
    print("Put your guess into Wordle and enter it below: ")
    guess = user_input()
    if re.fullmatch("[gyb]+", guess):
        print("Are you sure you meant to guess that? Remember, you are entering you guess, not a result. ")
        return guess_input()
    if len(guess) != 5 or not re.fullmatch("[a-z]{5}", guess):
        print("Your guess must be a five letter English word. ")
        return guess_input()
    return guess

def result_input(): 
    print("What did your guess yield? (g = green, y = yellow, b = blank/gray)")
    result = user_input()
    if len(result) != 5 or not re.fullmatch("[gyb]{5}", result):
        print("Your result must be a string of five g's, y's, and/or b's. For example: gbbyb. ")
        return result_input()
    return result

print("To start, we'll tell you what the best first Wordle guess is. ")
for turn in range(6): 
    print(f'The optimal guess is "{words.max_hits()[0]}."')
    print()
    guess = guess_input()
    result = result_input()
    if result == "ggggg":
        print("Congratulations, you won! ")
        print("Exiting Wordle solver. ")
        sys.exit()
    before_count = len(words.word_list)
    words.eliminate(guess, result)
    eliminated_count = before_count - len(words.word_list)
    print(f"Eliminated {eliminated_count} word{'' if eliminated_count == 1 else 's'}, or {eliminated_count/before_count * 100}% of all words. ")
    print()

print("Aw darn, you ran out of turns. But I'm sure you'll get 'em next time. ")
print("Exiting Wordle solver. ")    