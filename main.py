from Article import Article
from classifier import classify
import os

ARTICLE_LOCATION = 'developset/texts'
ANSWER_LOCATION = 'developset/answers'

def load_weapons():
    weapons = []
    lines = open(os.path.join(os.path.dirname(__file__), 'weapons.txt')).readlines()

    for line in lines:
        tokens = line.split(',')
        for token in tokens:
            weapons.append(token.strip().lower())

    return weapons

def read_weapons():
    weapons = set()
    for file_name in os.listdir(ANSWER_LOCATION):
        text = open(os.path.join(os.path.dirname(__file__), ANSWER_LOCATION + '/' + file_name)).readlines()
        for line in text:
            tokens = line.split(':')
            if tokens[0] == 'WEAPON':
                tokens[1] = tokens[1].strip()
                if tokens[1] != '-':
                    tokens = tokens[1].split('/')
                    for token in tokens:
                        weapons.add(token.strip().lower())

    print weapons

def main():
    for file_name in os.listdir(ARTICLE_LOCATION):
        text = open(os.path.join(os.path.dirname(__file__), ARTICLE_LOCATION + '/' + file_name)).readlines()
        article = Article(text)
        extracted_info = classify(article, load_weapons())


read_weapons()
