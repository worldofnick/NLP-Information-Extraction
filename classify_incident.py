import operator
import re

# Maps a phrase regex to a scaler multipler
arson_dict = {'arson': 4, 'arson(?=\s)': 1, 'houses\s+on\s+fire': 4, 'places\s+burned': 4, 'burning': 4, 'set\s+ablaze': 3, 'set\s+fire\s+to': 3,
'fires': 1}

attack_dict = { '(?<=\s)attack': 1, '(?<=\s)murder': 1, '(?<=\s)machine gun\s+attack': 3,
'(?<=\s)mortar': 3, '(?<=\s)shoot': 2, '(?<=\s)shot': 1, '(?<=\s)ARTILLERY\s+FIRE': 2, '(?<=\s)shoot\-out': 2,
'(?<=\s)firing\s+rockets': 3, '(?<=\s)launched\s+rockets': 3, '(?<=\s)fired\s+rocket': 2, '(?<=\s)firing': 1,
'(?<=\s)molotov': 4, '(?<=\s)assassinat': 2, '(?<=\s)massacre': 1}

bomb_dict = {'(?<=\s)bomb': 1, '(?<=\s)bombed rebel': 1, '(?<=\s)detonated': 5, '(?<=\s)explod': 2, '(?<=\s)explosi': 1,
'(?<=\s)placed\s+a\s+bomb': 3, '(?<=\s)car\s+bomb': 3, '(?<=\s)car\-bomb': 3, '(?<=\s)truck\s+bomb': 3,
'(?<=\s)explosive\s+device': 2, '(?<=\s)dynamite': 3, '(?<=\s)blowing\-up': 2, '(?<=\s)blew\-up': 2,
'(?<=\s)blown\s+up': 2, '(?<=\s)ied': 2, '(?<=\s)vbied': 2}

kidnap_dict = {'(?<=\s)kidnap': 4, '(?<=\s)abduct': 4, 'held\s+hostage': 4, 'hostage': 4, '(?<=\s)disappear': 1}

robbery_dict = {'(?<=\s)mugged': 1, '(?<=\s)stole(?=\s)': 1, '(?<=\s)steal': 1, '(?<=\s)robbery(?=\s)': 1, '(?<=\s)robbed(?=\s)': 1, '(?<=\s)burglar': 1, '(?<=\s)burglary': 1}

def score(text, dict):
    score = 0
    for pattern, scaler in dict.iteritems():
        match_count = len(re.findall(pattern, text, re.IGNORECASE | re.MULTILINE))
        score += match_count * scaler
    return score

def classify_inci(text):
    text = text.lower()
    score_dict = {}
    score_dict['ARSON'] = score(text, arson_dict)
    score_dict['ATTACK'] = score(text, attack_dict)
    score_dict['BOMBING'] = score(text, bomb_dict)
    score_dict['KIDNAPPING'] = score(text, kidnap_dict)
    score_dict['ROBBERY'] = score(text, robbery_dict)
    return max(score_dict.iteritems(), key=operator.itemgetter(1))[0]
