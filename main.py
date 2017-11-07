from __future__ import unicode_literals
from Article import Article
from classifier import classify
import os
import sys
import spacy
from spacy.en import English
import re
import ntpath
import cPickle

ARTICLE_LOCATION = 'developset/texts'
ANSWER_LOCATION = 'developset/answers'

en_nlp = English()

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
    weapons = load_text('weapons.txt')
    killingverbs = load_text('killingverbs.txt')
    orgs = load_text('orgs.txt')


    for line in lines:
        if is_header(line, headers):
            articles.append(line)
            currentIndex += 1
        else:
            articles[currentIndex] = articles[currentIndex] + ' ' + line.strip()

    # print '>> Loading casing model'
    file = open(ntpath.basename(input_path) + '.templates','w')
    # f = open(os.path.join(os.path.dirname(__file__), 'distributions.obj'))
    # uniDist = cPickle.load(f)
    # backwardBiDist = cPickle.load(f)
    # forwardBiDist = cPickle.load(f)
    # trigramDist = cPickle.load(f)
    # wordCasingLookup = cPickle.load(f)
    # f.close()
    # print '>> Loaded casing model'

    print ">> Beginning processing"
    count = 0
    for text in articles:
        print ">> Processing article " + str(count)
        article = Article(text)
        extracted_info = classify(article, weapons, killingverbs, orgs, en_nlp)
        extracted_info.write_template(file)
        count += 1

    print 'Successfully saved to ' + ntpath.basename(input_path) + '.templates'


main()
