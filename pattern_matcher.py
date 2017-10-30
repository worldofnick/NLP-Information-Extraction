import nltk
import numpy as np
from nltk import word_tokenize, pos_tag, ne_chunk

# Returns true if the sentence is in passive voice
def is_passive(tagged_sentence):
    passive_tags = [['VBZ', 'VBN'], ['VBP', 'VBN'],
    ['VBZ', 'VBG', 'VBN'], ['VBP', 'VBG', 'VBN'],
    ['VBZ', 'VBN', 'VBN'], ['VBP', 'VBN', 'VBN'],
    ['VBD', 'VBN'],
    ['VBD', 'VBG', 'VBN'],
    ['VBD', 'VBN', 'VBN'],
    ['MD', 'VB', 'VBN'],
    ['MD', 'VB', 'VBN', 'VBN']]

    tags = [word[1] for word in tagged_sentence]

    tags = np.array(tags)
    passive_tags = np.array(passive_tags)

    for passive_tag in passive_tags:
        if any((passive_tag == tags).all() for tags in passive_tag):
            return True

    return False


def find_matches(text):

    sent_text = nltk.sent_tokenize(text)
    perp = None
    victim = None
    for sentence in sent_text:
        tagged_sentence = pos_tag(word_tokenize(sentence))
