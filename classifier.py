from ExtractedInfo import ExtractedInfo
from classify_incident import classify_inci

def classify(article):
    incident_type = classify_inci(article.text)

    extracted_info = ExtractedInfo(article.id, incident_type, [], [], [], [], [])
    return extracted_info
