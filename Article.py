# Holds the text and the ID to the article.
from __future__ import unicode_literals
class Article:
    def __init__(self, text):
        self.id = text.split()[0]
        print self.id
        text = text[:len(self.id)]
        self.text = ' '.join(text)
