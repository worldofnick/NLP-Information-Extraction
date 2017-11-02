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


def find_victims(text, killing_verbs):
    sent_text = nltk.sent_tokenize(text.upper())
    victims = []

    for sentence in sent_text:
        en_nlp = English()
        doc = en_nlp(sentence)
        nlp_sentence = next(doc.sents)
        victims_root = []
        victims = []

        for np in doc.noun_chunks:
            if (np.root.head.lemma_ in killing_verbs and np.root.dep_ == 'nsubjpass') or np.root.head.text in victims_root:
                victims.append(np.text)
                victims_root.append(np.root.text)

    return victims





# import spacy
# from spacy.en import English

# nlp = English()
# doc = nlp(u'Nick and Brandon were killed by Ash')
# for np in doc.noun_chunks:
# 	print(np.text, np.root.dep_, np.root.head.text)
# 	# print np.dep_
# 	# print np.lemma_
# 	# print np.ent_type_
# 	print
# 	#print(np.text, np.root.text, np.root.dep_, np.root.head.text)

# def find_matches(sentence, patterns=[], targets=[]):

#
#     pos_tags = []
#
#     for i in range(0, len(nlp_sentence)):
# 		np = nlp_sentence[i]
# 		print np.tag_
# 		print np.dep_
# 		print np.ent_type_
#
# 		if np.dep_ == 'nsubjpass' and np.ent_type_ == 'PERSON':
# 			print 'Victim: ' + np.text
#
# 		elif np.dep_ == 'nsubjpass':
# 			print 'Target: ' + np.text
# 		print
#
#
#     pos_tag_string = ' '.join(pos_tags)
#     print pos_tag_string
#
#
#
#
# sentence = u'Nick, Adam, and Ash were bombed'
#
#
# find_matches(sentence)
