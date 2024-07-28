"""Random Words Generator

This script creates random words with a desired
number of counts.
"""
import numpy as np
from RandomWordGenerator import RandomWord


max_freq = 600
word_counts = np.floor(max_freq / np.arange(1, max_freq + 1))
rw = RandomWord()
random_words = rw.getList(num_of_words=max_freq)
writer = open('test_data/random_words.txt', 'w')
for index in range(max_freq):
    count = int(word_counts[index])
    word_sequence = f'{random_words[index]} ' * count
    writer.write(word_sequence + '\n')
writer.close()
