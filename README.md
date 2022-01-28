# wordle-analysis
This is a crude analysis of the Wordle word game. 

We find that, for a first turn guess: 
- "realo" optimizes for the greatest number of yellows and greens. 
- "saree" optimizes for the greatest number of greens.
- "opera" optimizes for the greatest number of yellows.

Note that this data is only based on the list of potential guesses available on the Wordle website. There is a separate, smaller list containing all possible solutions that I did not look at because I believe that running analysis on the actual Wordle solutions would constitute cheating. For the purposes of this project, the list of Wordle solutions is composed of every valid Wordle guess that does not end in an "s." My failure to use the actual list of solutions means that the estimates and strategies derived from a default application of this code are necessarily imperfect. However, if you find the list of actual solutions, you can plug them into the program relatively easily and get a more accurate result. 

## Contents
- wordle_words.txt is a list of all Wordle guesses, pulled from the Wordle website
- position_frequencies_n.txt gives a sorted list of letters based on the proportion of Wordle solutions where they appear in position n. 
- word_frequencies_count_n.txt gives a sorted list of letters based on the proportion of Wordle solutions where they appear at least n times. 
- words_average_greens.txt is a sorted list of Wordle guesses by the average number of greens each gives when guessed across every Wordle solution. Ties (or near ties) are broken by the average number of yellows.
- words_average_yellows.txt is a sorted list of Wordle guesses by the average number of yellows each gives when guessed across every Wordle solution. Ties (or near ties) are broken by the average number of greens.
- words_average_hits.txt is a sorted list of Wordle guesses by the average number of hits (greens and yellows) each gives when guessed across every Wordle solution. Ties (or near ties) are broken by the average number of greens.
- wordle_solver.py is a crude, interactive, text-based solver that attempts to optimize guesses by mazimizing the greatest number of eliminated solutions. Its recommendations are less threshed out than our first guess recommendations.

