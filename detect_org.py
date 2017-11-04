from __future__ import unicode_literals
import spacy
from spacy.en import English

def detect_orgs(text):
    nlp = English()
    doc = nlp(text)
    orgs = []
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            orgs.append(ent.text)

    return orgs
