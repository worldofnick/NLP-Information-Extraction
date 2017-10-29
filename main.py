from Article import Article
from text_preprocess import preprocess
import os


ARTICLE_LOCATION = 'developset/texts'

def main():
    for file_name in os.listdir(ARTICLE_LOCATION):
        text = open(os.path.join(os.path.dirname(__file__), ARTICLE_LOCATION + '/' + file_name)).readlines()
        article = Article(text)
        preprocess(article.text)
        break
        # We can either store all articles, or process them in a streaming matter

        # extracted_info = extract(article)
        # Use ExtractedInfo.py to write to file

main()
