from Article import Article
from classifier import classify
import os

ARTICLE_LOCATION = 'developset/texts'

def main():
    for file_name in os.listdir(ARTICLE_LOCATION):
        text = open(os.path.join(os.path.dirname(__file__), ARTICLE_LOCATION + '/' + file_name)).readlines()
        article = Article(text)
        extracted_info = classify(article)
        

main()
