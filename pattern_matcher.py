import ntlk
from nltk import word_tokenize, pos_tag, ne_chunk

def is_passive(tagged_sentence):
    passive_tags = [['VBZ', 'VBN'], ['VBP', 'VBN'],
    ['VBZ', 'VBG', 'VBN'], ['VBP', 'VBG', 'VBN'],
    ['VBZ', 'VBN', 'VBN'], ['VBP', 'VBN', 'VBN'],
    ['VBD', 'VBN'],
    ['VBD', 'VBG', 'VBN'],
    ['VBD', 'VBN', 'VBN'],
    ['MD', 'VB', 'VBN'],
    ['MD', 'VB', 'VBN', 'VBN']]

    return False


def find_matches(text):

    sent_text = nltk.sent_tokenize(text)
    perp = None
    victim = None
    for sentence in sent_text:
        tagged_sentence = ne_chunk(pos_tag(word_tokenize(sentence)))
