from __future__ import unicode_literals
from ExtractedInfo import ExtractedInfo
from classify_incident import classify_inci
from detect_weapons import extract_weapons
from pattern_matcher import find_victims
from detect_org import detect_orgs
from detect_perp_individual import detect_individuals
from detect_targets import detect_targets

def classify(article, common_weapons, killing_verbs, en_nlp):
    incident_type = classify_inci(article.text)
    weapons = extract_weapons(article.text, common_weapons)
    orgs = detect_orgs(article.text, killing_verbs, en_nlp)
    targets = detect_targets(article.text, killing_verbs, en_nlp)
    # victims = find_victims(article.text, killing_verbs, en_nlp)
    individuals = detect_individuals(article.text, killing_verbs, en_nlp)

    # return ExtractedInfo(article.id, incident_type, weapons, [], [], [], victims)
    return ExtractedInfo(article.id, incident_type, weapons, individuals, orgs, targets, [])
    # return ExtractedInfo(article.id, incident_type, weapons, [], [], [], victims)
    # return ExtractedInfo(article.id, "-", [], [], [], [], victims)
