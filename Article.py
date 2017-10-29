# Holds the text and the ID to the article.

class Article:
    def __init__(self, text):
        self.TEXT_MARKER = '[TEXT]'
        self.id = text[0].split()[0]

        text.pop(0)
        # for i in range(0, len(text)):
        #     text[i] = text[i].strip()
        #
        self.text = ' '.join(text)
        # date_index = self.text.index(self.TEXT_MARKER)
        # self.text = self.text[date_index + len(self.TEXT_MARKER) + 1:]
