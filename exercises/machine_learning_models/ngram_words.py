import string


def read_file(filename: str, max_line_count: int) -> list:
    content = []
    with open(filename, 'r') as file:
        count = 0
        while count < max_line_count:
            line = file.readline()
            if not line:
                break
            content.append(line.strip())
            count += 1
    
    return content

def data_normalization(content: list) -> list:
    normalized_content = []
    for sentence in content:
        words = sentence.split(' ')
        normalized_words = []
        
        # Normalizate each word
        # 1. Remove '-LRB-' and '-RRB-'
        # 2. Remove unascii word
        # 3. Remove punctuation
        for word in words:
            if word == '-LRB-' or word == '-RRB-':
                word = ''
            elif word in string.punctuation:
                word = ''
            elif not word.isascii():
                word = ''
            
            if word != '':
                normalized_words.append(word)        
        normalized_sentence = ' '.join(normalized_words)
        normalized_content.append(normalized_sentence)
    return normalized_content

def add_token(content: list[str], starts: int, ends: int) -> list[str]:
    tokenized_content = []
    
    for sentence in content:
        tokenized_content.append('START ' * starts + sentence + ' END' * ends)
    
    return tokenized_content

def n_gram_words(content: list, n: int) -> dict:
    vocab = {}
    for sentence in content:
        words = sentence.split(' ')
        for i in range(len(words) - n + 1):
            n_gram = tuple(words[i: i + n])
            vocab.setdefault(n_gram, 0)
            vocab[n_gram] += 1
    
    return vocab

def write_ngram_to_file(vocab: dict, filename: str) -> None:
    with open(filename, 'a') as file:
        for key, value in vocab.items():
            key = ' '.join(key)
            value = str(value)
            file.write('\t'.join([value, key]) + '\n')

def data_prepare_for_ngram(data_filename: str, vocab_filename: str, n: int, type: str = 'markov') -> dict:
    content = read_file(data_filename, 10000)
    vocabs = {}
    content = data_normalization(content)
    
    if type.lower() == 'markov':
        # Generate ngram and n-1 gram vocab
        content = add_token(content, n-1, 1)
        for i in range(n-1, n+1):
            vocab = n_gram_words(content, i)
            write_ngram_to_file(vocab, vocab_filename)
            vocabs.update(vocab)
    elif type.lower() == 'chainrule':
        # Generate 1, 2, ..., n+1 gram vocab, include start and end token
        content = add_token(content, 1, 1)
        for i in range(1, n+1):
            vocab = n_gram_words(content, i)
            write_ngram_to_file(vocab, vocab_filename)
            vocabs.update(vocab)
    
    return vocabs
