# wordle-analysis
This is a crude analysis of the Wordle word game. 

We find that, for a first turn guess: 
- "aeros" optimizes for the greatest number of yellows and greens. 
- "sores" optimizes for the greatest number of greens.
- "estro" optimizes for the greatest number of yellows.

## Contents
- wordle_words.txt is a list of all Wordle words, pulled from the Wordle website
- position_frequencies_n.txt gives a sorted list of letters based on the proportion of Wordle words where they appear in position n. 
- word_frequencies_count_n.txt gives a sorted list of letters based on the proportion of Wordle words where they appear at least n times. 
- words_average_greens.txt is a sorted list of Wordle words by the average number of greens each gives when guessed across every Wordle word. Ties (or near ties) are broken by the average number of yellows.
- words_average_yellows.txt is a sorted list of Wordle words by the average number of yellows each gives when guessed across every Wordle word. Ties (or near ties) are broken by the average number of greens.
- words_average_hits.txt is a sorted list of Wordle words by the average number of hits (greens and yellows) each gives when guessed across every Wordle word. Ties (or near ties) are broken by the average number of greens.
- wordle_solver.py is a crude, interactive, text-based solver that attempts to optimize guesses by mazimizing the greatest number of eliminated words. Its recommendations are less threshed out than our first guess recommendations.

