from pathlib import Path
from ngram_words import data_prepare_for_ngram


directory = Path(__file__).resolve().parent / 'data'
data_filename = Path(directory) / 'data.movie.sample.txt'
vocab_filename = Path(directory) / 'data.movie.ngrams.txt'

vocabs = data_prepare_for_ngram(data_filename, vocab_filename, 2)