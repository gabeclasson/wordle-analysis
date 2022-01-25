from itertools import product
from string import ascii_lowercase
import re
from Wordle import *
from functools import cmp_to_key


class Words: 
    def __init__(self, possible_solutions, possible_guesses, word_length, hard_mode=False):
        self.word_length = word_length
        self.frequency_by_position = [ {letter: 0 for letter in ascii_lowercase} for i in range(word_length) ]
        self.frequency_among_solutions = [ {letter: 0 for letter in ascii_lowercase} for i in range(word_length) ]
        self.hard_mode = hard_mode
        self.possible_guesses = possible_guesses[:]
        
        possible_solutions = list(filter(lambda word: len(word) == word_length, possible_solutions))
        possible_solutions = list(map(lambda str: str.lower(), possible_solutions))
        possible_solutions = list(set(possible_solutions))
        self.possible_solutions = []
        self.size = 0
        for word in possible_solutions:
            self.add_possible_solution(word)

    @classmethod
    def default_config(cls, hard_mode=False):
        word_file = open("wordle_words.txt")
        words = word_file.readlines()
        words = [word[:-1] for word in words]
        possible_solutions = [word for word in words if word[-1] != "s"]
        return cls(possible_solutions, words, 5, hard_mode=hard_mode)


    def add_possible_solution(self, word):
        assert len(word) == self.word_length
        self.possible_solutions.append(word)
        for position, letter in enumerate(word):
            self.frequency_by_position[position][letter] += 1
            self.frequency_among_solutions[word[:position].count(letter)][letter] += 1
        self.size += 1      

    def remove_possible_solution(self, word):
        self.possible_solutions.remove(word)
        for position, letter in enumerate(word):
            self.frequency_by_position[position][letter] -= 1
            self.frequency_among_solutions[word[:position].count(letter)][letter] -= 1 
        self.size -= 1

    def remove_guess(self, word): 
        self.possible_guesses.remove(word)

    # The number of solutions in the corpus that have a letter in a particular position
    def letter_frequency_by_position(self, letter, position):
        return self.frequency_by_position[position][letter]

    # The number of solutions in which num instances of a given letter appear
    def letter_frequency_among_solutions(self, letter, num=1): 
        return self.frequency_among_solutions[num - 1][letter]

    # The portion of solutions in the corpus that have a letter in a particular position
    def letter_relative_frequency_by_position(self, letter, position):
        return self.letter_frequency_by_position(letter, position) / self.size

    # The portion of solutions in the corpus in which num instances of a given letter appear
    def letter_relative_frequency_among_solutions(self, letter, num=1):
        return self.letter_frequency_among_solutions(letter, num) / self.size

    # The expected portion of solutions that will be eliminated by guessing this word. 
    def expected_elimination(self, word):
        expected_elimination = 0

        # Duplicate letters in a word increase the green expected eliminations, but not the yellow and 
        for position, letter in enumerate(word): 
            rel_freq_pos = self.letter_relative_frequency_by_position(letter, position)
            rel_freq_tot = self.letter_relative_frequency_among_solutions(letter)

            # When a letter is green, you will remove all words that do not have a letter in that position
            probability_green = rel_freq_pos
            portion_removed_green = 1 - probability_green
            expected_elimination += probability_green * portion_removed_green

            # When a letter is yellow, you will remove all words that do not contain that letter
            count = word[:position + 1].count(letter)
            probability_yellow = self.letter_relative_frequency_among_solutions(letter, count) - probability_green
            portion_removed_yellow = 1 - rel_freq_tot
            expected_elimination += probability_yellow * portion_removed_yellow

            # When a letter is gray, you will remove all words that contain that letter
            portion_removed_gray = probability_green + probability_yellow
            probability_gray = 1 - portion_removed_gray
            expected_elimination += probability_gray * portion_removed_gray

        return expected_elimination

    def best_guess_ee(self):
        return max(self.possible_guesses, key=lambda word: self.expected_elimination(word))

    # gives the average number of "hits" (greens and yellows) that a particular guess yields
    def average_hits(self, guess):
        hits = 0
        for position, letter in enumerate(guess):
            count = guess[:position + 1].count(letter)
            hits += self.letter_frequency_among_solutions(letter, count)
        return hits / self.size      

    # Gives a tuple containing a guess and its average "hits" (greens and yellows)
    def max_hits(self):
        tuples = [(word, self.average_hits(word)) for word in self.possible_guesses]
        return max(tuples, key=self.tuple_sort_key(tie_break_greens=True))

    def sorted_guesses_hits(self, length=100, descending=True):
        tuples = [(word, self.average_hits(word)) for word in self.possible_guesses]
        return sorted(tuples, reverse=descending, key=self.tuple_sort_key(tie_break_greens=True))[:length]

    def average_greens(self, guess):
        greens = 0
        for pos, letter in enumerate(guess): 
            greens += self.letter_frequency_by_position(letter, pos)
        return greens/self.size

    def max_greens(self):
        tuples = [(word, self.average_greens(word)) for word in self.possible_guesses]
        return max(tuples, key=self.tuple_sort_key(tie_break_greens=False))

    def sorted_potential_guesses_greens(self, length=100, descending=True):
        tuples = [(word, self.average_greens(word)) for word in self.possible_guesses]
        return sorted(tuples, reverse=descending, key=self.tuple_sort_key(tie_break_greens=False))[:length]

    def average_yellows(self, guess):
        return self.average_hits(guess) - self.average_greens(guess)

    def max_yellows(self):
        tuples = [(word, self.average_yellows(word)) for word in self.possible_guesses]
        return max(tuples, key=self.tuple_sort_key(tie_break_greens=True))

    def sorted_potential_guesses_yellows(self, length=100, descending=True):
        tuples = [(word, self.average_yellows(word)) for word in self.possible_guesses]
        return sorted(tuples, reverse=descending, key=self.tuple_sort_key(tie_break_greens=True))[:length]

    # Gives the average numbers of greens and yellows (g, y) that this guess gives when compared to all other words in the cohort. 
    def average_result(self, guess): 
        return self.average_greens(guess), self.average_yellows(guess)

    # Gives a single number representing the weighted average of. By default, weights based on total hits (green and yellow equally)
    def weighted_average_result(self, guess, green=1, yellow=1):
        greens, yellows = self.average_result(guess)
        return green * greens + yellow * yellows

    # Returns a comparison function that compares two tuples, where the first element of each is a word and the second element is a number
    def tuple_sort_key(self, tie_break_greens): 
        @cmp_to_key
        def compare_words(tup1, tup2):
            word, weighted_avg = tup1
            other_word, other_weighted_avg = tup2
            if abs(weighted_avg - other_weighted_avg) > 0.0000000001:
                return weighted_avg - other_weighted_avg
            if tie_break_greens: 
                return self.average_greens(word) - self.average_greens(other_word)
            else: 
                return self.average_yellows(word) - self.average_yellows(other_word)
        
        return compare_words

    # Sorts guesses by their weighted average result
    def sorted_potential_guesses(self, green=1, yellow=1, length=100, descending=True, tie_break_greens = True): 
        tuples = [(word, self.weighted_average_result(word, green, yellow)) for word in self.possible_guesses]
        return sorted(tuples, reverse=descending, key=self.tuple_sort_key(tie_break_greens))[:length]

    # Eliminates from the list of words every word that does not conform to the result
    def eliminate(self, guess, result):
        assert len(guess) == self.word_length and len(result) == self.word_length, "Result string must match word length."
        for test_word in self.possible_solutions[:]:
            if wordle_result(guess, test_word) != result: 
                self.remove_possible_solution(test_word)
        if self.hard_mode: 
            for test_guess in self.possible_guesses[:]:
                if valid_guess_hard_mode(test_guess, guess, result): 
                    self.possible_guesses.remove(test_guess)

    
    # Gives a list of tuples (letter, relative_frequency), where relative_frequency is the relative frequency of each letter in the given position
    def sorted_letters_by_position(self, position, descending=True):
        tuples = [(letter, self.letter_relative_frequency_by_position(letter, position)) for letter in ascii_lowercase]
        return sorted(tuples, reverse=descending, key=lambda tup: tup[1])

    def sorted_letters_by_count(self, count, descending=True):
        tuples = [(letter, self.letter_relative_frequency_among_solutions(letter, count)) for letter in ascii_lowercase]
        return sorted(tuples, reverse=descending, key=lambda tup: tup[1])

    # Takes an iterable of iterables and writes row by row, column by column, tab separated to file
    def write_table_to_file(self, path, table): 
        file = open(path, "a")
        for row in table: 
            file.write("    ".join(str(item) for item in row) + "\n")
        file.close()

    def export_position_frequencies(self): 
        for i in range(self.word_length): 
            self.write_table_to_file(f"position_frequencies_{i}.txt", self.sorted_letters_by_position(i))

    def export_word_frequencies(self): 
        for num in range(1, self.word_length + 1): 
            self.write_table_to_file(f"word_frequencies_count_{num}.txt", self.sorted_letters_by_count(num))

    def export_word_averages(self):  
        self.write_table_to_file(f"words_average_greens.txt", self.sorted_potential_guesses_greens(length=100000000000))
        self.write_table_to_file(f"words_average_yellows.txt", self.sorted_potential_guesses_yellows(length=100000000000))
        self.write_table_to_file(f"words_average_hits.txt", self.sorted_guesses_hits(length=100000000000))

words = Words.default_config()