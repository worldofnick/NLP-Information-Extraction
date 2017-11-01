# Holds the text and the ID to the article.
from __future__ import unicode_literals
class Article:
    def __init__(self, text):
        self.id = text[0].split()[0]

        text.pop(0)
        self.text = ' '.join(text)
