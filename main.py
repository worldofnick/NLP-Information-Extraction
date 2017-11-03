from __future__ import unicode_literals
from Article import Article
from classifier import classify
import os
import sys
import re
import ntpath

ARTICLE_LOCATION = 'developset/texts'
ANSWER_LOCATION = 'developset/answers'

def load_text(file_name):
    weapons = set()
    lines = open(os.path.join(os.path.dirname(__file__), file_name)).readlines()

    for line in lines:
        tokens = line.split(',')
        for token in tokens:
            weapons.add(token.strip().upper())

    return weapons

def is_header(line, headers):
    for header in headers:
        if header in line:
            return True

    return False

def main():

    input_path = sys.argv[1]

    lines = open(input_path).readlines()
    headers = ['DEV-MUC3', 'TST1-MUC3', 'TST2-MUC4']
    articles = []
    currentIndex = -1

    for line in lines:
        if is_header(line, headers):
            articles.append(line)
            currentIndex += 1
        else:
            articles[currentIndex] = articles[currentIndex] + ' ' + line.strip()


    file = open(ntpath.basename(input_path) + '.templates','w')
    for text in articles:
        article = Article(text)
        extracted_info = classify(article, load_text('weapons.txt'), load_text('killingverbs.txt'))
        extracted_info.write_template(file)


main()
