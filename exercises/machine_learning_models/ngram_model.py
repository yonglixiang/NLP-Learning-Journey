from pathlib import Path
import math

from ngram_words import data_prepare_for_ngram

class NGram():
    def __init__(self, ngram_path: str, model_type: str, n: int=2) -> None:
        '''
        ngram_path: the filepath to read the ngrams
        model_type: either 'markov' or 'chainrule'
        '''
        self.model_type = model_type
        self.n = n
        
        self.ngrams = {}
        with open (ngram_path, 'r') as file:
            for line in file:
                count, ngram = line.strip().split('\t')
                count = int(count)
                ngram = tuple(ngram.split())
                self.ngrams.setdefault(ngram, 0)
                self.ngrams[ngram] += count
                
    def cal_prob_by_chainrule(self, query: str) -> float:
        ngrams = self.ngrams
        query = 'START ' + query + ' END'
        
        logprob = 0
        words = query.split(' ')
        for i in range(len(words), 1, -1):
            full, context = tuple(words[:i]), tuple(words[:i-1])
            count_full, count_context = ngrams.get(full, 0), ngrams.get(context, 0)
            
            if count_full == 0 or count_context == 0:
                return 0
            
            prob = count_full / count_context
            logprob += math.log(prob)
        
        return math.exp(logprob)

    def cal_prob_by_markov(self, query: str) -> float:
        ngrams = self.ngrams
        n = self.n
        query = 'START ' * (n-1) + query + ' END'
        
        words = query.split(' ')
        logprob = 0
        
        for i in range(len(words)-n+1):
            full, context = tuple(words[i: i+n]), tuple(words[i: i+n-1])
            count_full, count_context = ngrams.get(full, 0), ngrams.get(context, 0)
            
            if count_full == 0 or count_context == 0:
                return 0
            
            prob = count_full / count_context
            logprob += math.log(prob)
        
        return math.exp(logprob)

    def cal_prob_by_markov_with_discounting(self, query: str, discount: float):
        ngrams = self.ngrams
        n = self.n
        query = 'START ' * (n-1) + query + ' END'
        
        words = query.split(' ')
        seen = {}
        vocabs = set()
        logprob = 0
        
        for ngram, count in ngrams.items():
            if len(ngram) == n:
                seen.setdefault(ngram[:-1], set())
                seen[ngram[:-1]].add(ngram[-1])
            for vocab in ngram:
                if vocab != 'START':
                    vocabs.add(vocab)
        
        for i in range(len(words)-n+1):
            full, context = tuple(words[i: i+n]), tuple(words[i: i+n-1])
            count_full, count_context = ngrams.get(full, 0), ngrams.get(context, 0)
            
            if count_full != 0:
                prob = (count_full - discount)/ count_context
                if prob == 0:
                    return 0
                logprob += math.log(prob)
            elif context not in seen:
                prob = 1 / len(vocabs)
                logprob += math.log(prob)
            else:
                seen_word = seen[context]
                available_prob = len(seen_word) * (discount / count_context)
                prob = available_prob / (len(vocabs) - len(seen_word))
                if prob == 0:
                    return 0
                logprob += math.log(prob)
                
        return math.exp(logprob)
    
    def cal_prob_by_markov_with_interplotion(self, query: str, weights: list[float]):
        '''
        weights: should order from ngram to unigram, e.g. [4-gram weight, trigram weight, bigram weight, unigram weight]
        '''
        ngrams = self.ngrams
        n = self.n
        query = 'START ' * (n-1) + query + ' END'
        
        words = query.split(' ')
        logprob = 0
        vocab_total = 0
        
        for ngram, count in ngrams.items():
            if(len(ngram)) == 1 and ngram != ('START', ):
                vocab_total += count
                    
        
        for i in range(len(words)-n+1):
            j = 0
            prob = 0
            for weight in weights:
                # unigram, prob = count of current word / count of all single worrd
                if j == n-1:
                    unigram = tuple(words[i+n-1: i+n])
                    count_full, count_context = ngrams.get(unigram, 0), vocab_total
                else:
                    full, context = tuple(words[i+j: i+n]), tuple(words[i+j: i+n-1])
                    count_full, count_context = ngrams.get(full, 0), ngrams.get(context, 0)
                
                if count_context != 0:
                    prob += weight * (count_full / count_context)
                j += 1

            if prob == 0:
                return 0
            logprob += math.log(prob)
            
        return math.exp(logprob)
    
def main():
    directory = Path(__file__).resolve().parent / 'data'
    data_filename = Path(directory) / 'data.movie.sample.txt'
    ngram_filename = Path(directory) / 'data.movie.ngrams.txt'
    data_prepare_for_ngram(data_filename, ngram_filename, 3)
    
    n = 3
    query = "I eat NLP"
    discount = 0.1
    weights = [0.4, 0.4, 0.2]
    
    trigram_i = NGram(ngram_filename, 'markov', n)
    
    print(trigram_i.cal_prob_by_markov_with_interplotion(query, weights))

main()
