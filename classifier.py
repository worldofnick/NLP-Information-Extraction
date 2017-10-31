
from ExtractedInfo import ExtractedInfo
from classify_incident import classify_inci
from detect_weapons import extract_weapons

def classify(article, common_weapons):
    incident_type = classify_inci(article.text)
    weapons = extract_weapons(article.text, common_weapons)


    extracted_info = ExtractedInfo(article.id, incident_type, [], [], [], [], [])
    return extracted_info
