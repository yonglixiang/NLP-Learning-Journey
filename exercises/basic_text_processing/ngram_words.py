from pathlib import Path


def read_sentence(filename: str, directory: str, max_count: int) -> list:
    content = []
    file_path = Path(directory) / filename
    
    with file_path.open('r') as file:
        count = 0
        while count < max_count:
            line = file.readline()
            if not line:
                break
            parts = line.split('\t')
            if len(parts) < 2:
                continue  # Skip lines that don't have the expected format
            num, sentence = parts
            content.append(sentence.strip())
            count += 1
    
    return content

def normalization(content: list) -> list:
    normalized_content = []
    for sentence in content:
        words = sentence.split(' ')
        normalized_words = []
        for word in words:
            if word == '-LRB-':
                word = '('
            elif word == '-RRB-':
                word = ')'
            elif not word.isascii():
                word = ''
            else:
                word = word.lower()
            
            if word != '':
                normalized_words.append(word)
        normalized_sentence = ' '.join(normalized_words)
        normalized_content.append(normalized_sentence)
    return normalized_content

def n_gram_words(content: list, n: int) -> dict:
    vocab = {}
    
    for sentence in content:
        words = sentence.split(' ')
        for i in range(len(words) - n + 1):
            n_gram = tuple(words[i: i + n])
            vocab.setdefault(n_gram, 0)
            vocab[n_gram] += 1
    
    return vocab
