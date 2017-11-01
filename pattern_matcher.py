from __future__ import unicode_literals
import nltk
import numpy as np
import spacy
from spacy.en import English

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


def find_victims(text):
    sent_text = nltk.sent_tokenize(text.lower())
    victim = None

    for sentence in sent_text:
        en_nlp = English()
        doc = en_nlp(sentence)
        sentence = next(doc.sents)

        for i in range(0, len(sentence) - 1):
            prev_word = 'PHI'
            if i > 0:
                prev_word = sentence[i - 1]

            next_word = sentence[i + 1]
            word = sentence[i]
            if word.dep_ == 'nsubj':
                print prev_word.text
                #print "%s:%s" % (word, word.dep_)
                print word.text
                print next_word.text
                print

    return []
