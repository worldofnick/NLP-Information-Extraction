import re, nltk

patterns = ['(.+)\s+was\s+killed', '(.+)\s+was\s+shot', '(.+)\s+was\s+stabbed', '(.+)\s+was\s+murdered', '(.+)\s+was\s+fatality']

def detect_victims(article_text):
    victims = set()
    titlecase_article_text = article_text.lower()
    tokenized_sents = nltk.sent_tokenize(titlecase_article_text)

    for sentence in tokenized_sents:
        for pattern in patterns:
            matches = re.findall(pattern, sentence, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                match = matches[0].split()
                if len(match) > 1:
                    victims.add(match[-2].upper() + ' ' + match[-1].upper())



    return victims
