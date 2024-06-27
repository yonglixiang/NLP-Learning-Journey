from pathlib import Path
import math

from ngram_words import data_prepare_for_ngram


def cal_prob_by_chainrule(vocabs: dict, query: str) -> float:
    logprob = 0
    words = query.split(' ')
    for i in range(len(words), 1, -1):
        full, context = tuple(words[:i]), tuple(words[:i-1])
        count_full, count_context = vocabs.get(full, 1), vocabs.get(context, 1000)
        logprob += math.log(count_full / count_context)
        
        print(full, count_full, context, count_context)
    
    return math.exp(logprob)

def cal_prob_by_markov(vocabs: dict, query: str, n: int) -> float:
    words = query.split(' ')
    logprob = 0
    
    for i in range(len(words)-n+1):
        full, context = tuple(words[i: i+n]), tuple(words[i: i+n-1])
        count_full, count_context = vocabs.get(full, 1), vocabs.get(context, 1000)
        logprob += math.log(count_full / count_context)

        print(full, count_full, context, count_context)
    return math.exp(logprob)
        
    
def main():
    directory = Path(__file__).resolve().parent / 'data'
    data_filename = Path(directory) / 'data.movie.sample.txt'
    vocab_filename = Path(directory) / 'data.movie.ngrams.txt'
    
    type = 'markov'
    n = 3
    query = "I love NLP"
    
    if type == 'markov':
        query = 'START ' * (n-1) + query + ' END'
        vocabs = data_prepare_for_ngram(data_filename, vocab_filename, n, type)
        cal_prob_by_markov(vocabs, query, n)
    elif type == 'chainrule':
        query = 'START ' + query + ' END'
        vocabs = data_prepare_for_ngram(data_filename, vocab_filename, len(query.split(' ')), type)
        cal_prob_by_chainrule(vocabs, query)

main()
    

