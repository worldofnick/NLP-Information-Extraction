from __future__ import unicode_literals
from nltk.tokenize import sent_tokenize, word_tokenize

def extract_weapons(text, common_weapons):
    sent_tokenize_list = sent_tokenize(text.upper())
    weapons = set()

    for sentence in sent_tokenize_list:
        words = word_tokenize(sentence)
        for common_weapon in common_weapons:
            if common_weapon.upper() in words:
                weapons.add(common_weapon)

    return weapons
