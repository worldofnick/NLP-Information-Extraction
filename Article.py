# Holds the text and the ID to the article.
from __future__ import unicode_literals
from Truecaser import *
import nltk

class Article:
    def __init__(self, text, uniDist, backwardBiDist, forwardBiDist, trigramDist, wordCasingLookup):
        self.id = text.split()[0]
        text = text[len(self.id):]
        self.text = text
        self.uniDist = uniDist
        self.backwardBiDist = backwardBiDist
        self.forwardBiDist = forwardBiDist
        self.trigramDist = trigramDist
        self.wordCasingLookup = wordCasingLookup
        self.cased_text = self.fix_casing(text)
        print self.cased_text

    def fix_casing(self, text):
        cased_text = ''
        sent_tokenize_list = nltk.sent_tokenize(text)
        for sentence in sent_tokenize_list:
            tokens_correct = nltk.word_tokenize(sentence)
            tokens = [token.lower() for token in tokens_correct]
            tokensTrueCase = getTrueCase(tokens, 'title', self.wordCasingLookup, self.uniDist, self.backwardBiDist, self.forwardBiDist, self.trigramDist)

            # Group puncuation with word
            puncuated_tokens = []
            count = 0
            for token in tokensTrueCase:
                if token in string.punctuation and count != 0:
                    puncuated_tokens[count - 1] = puncuated_tokens[count - 1] + token
                else:
                    puncuated_tokens.append(token)
                    count += 1


            cased_text += ' ' + ' '.join(puncuated_tokens)

        return cased_text
