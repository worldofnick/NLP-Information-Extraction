from __future__ import unicode_literals
from ExtractedInfo import ExtractedInfo
from classify_incident import classify_inci
from detect_weapons import extract_weapons
from pattern_matcher import find_victims
from detect_org import detect_orgs
from detect_targets import detect_targets

def classify(article, common_weapons, killing_verbs):
    incident_type = classify_inci(article.text)
    weapons = extract_weapons(article.text, common_weapons)
    orgs = detect_orgs(article.text, killing_verbs)
    targets = detect_targets(article.text, killing_verbs)
    # victims = find_victims(article.text, killing_verbs)

    # return ExtractedInfo(article.id, incident_type, weapons, [], [], [], victims)
    return ExtractedInfo(article.id, incident_type, weapons, [], orgs, targets, [])
    # return ExtractedInfo(article.id, incident_type, weapons, [], [], [], victims)
    # return ExtractedInfo(article.id, "-", [], [], [], [], victims)
