from __future__ import unicode_literals
from ExtractedInfo import ExtractedInfo
from classify_incident import classify_inci
from detect_weapons import extract_weapons
from pattern_matcher import find_victims

def classify(article, common_weapons):
    incident_type = classify_inci(article.text)
    weapons = extract_weapons(article.text, common_weapons)
    victims = find_victims(article.text)

    extracted_info = ExtractedInfo(article.id, incident_type, [], [], [], [], [])
    return extracted_info
