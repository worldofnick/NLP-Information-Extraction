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

# sentence procssed by spacy
def capitalize_nouns(setence):
    words = []
    noun_tags = ['NOUN', 'PROPN']
    for token in sentence:
        if token.pos_ in noun_tags:
            words.append(token.text_.title())

    return ' '.join(words)

def find_victims(text, killing_verbs):
    sent_text = nltk.sent_tokenize(text.upper())
    victims = []
    targets = []

    for sentence in sent_text:
        en_nlp = English()
        doc = en_nlp(sentence)
        sentence = next(doc.sents)

        for token in sentence:
            if token.dep_ == 'ROOT' and token.lemma_ in killing_verbs:
                killing_verb = token.text_
                # Someone dies in this sentence
                # Capitalize all nouns in sentence
                cap_sentence = capitalize_nouns(sentence)
                sentence_doc = en_nlp.make_doc(cap_sentence)
                # NER
                for word in sentence_doc:
                    # Is this word a person and connected to the root verb?
                    if word.ent_type_ == 'PERSON' and word.root.head.text == killing_verb and

                # Take into account conjunctions

                # If NER result is place make target
                # If NER result is person make it victim

    return []





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
#     en_nlp = English()
#     doc = en_nlp(sentence)
#     nlp_sentence = next(doc.sents)
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
