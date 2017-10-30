import operator
import re

# Maps a phrase regex to a scaler multipler
arson_dict = {'arson': 1, 'arson(?=\s)': 1, 'houses\s+on\s+fire': 4, 'places\s+burned': 4, 'burning': 4, 'set\s+ablaze': 2, 'set\s+fire\s+to': 3,
'fires': 1}

attack_dict = {'(dynamite|bomb|bombing)\s+attack': 1, '(?<=\s)attack': 1, '(?<=\s)murder': 1, '(?<=\s)machine gun\s+attack': 3,
'(?<=\s)mortar': 3, '(?<=\s)shoot': 2, '(?<=\s)shot': 1, '(?<=\s)ARTILLERY\s+FIRE': 2, '(?<=\s)shoot\-out': 2,
'(?<=\s)firing\s+rockets': 3, '(?<=\s)launched\s+rockets': 3, '(?<=\s)fired\s+rocket': 2, '(?<=\s)firing': 1,
'(?<=\s)molotov': 4, '(?<=\s)assassinat': 2, '(?<=\s)massacre': 1}

bomb_dict = {'(?<=\s)bomb': 1, '(?<=\s)bombed rebel': 1, '(?<=\s)detonated': 5, '(?<=\s)explod': 2, '(?<=\s)explosi': 1,
'(?<=\s)placed\s+a\s+bomb': 3, '(?<=\s)car\s+bomb': 3, '(?<=\s)car\-bomb': 3, '(?<=\s)truck\s+bomb': 3,
'(?<=\s)explosive\s+device': 2, '(?<=\s)dynamite': 3, '(?<=\s)blowing\-up': 2, '(?<=\s)blew\-up': 2,
'(?<=\s)blown\s+up': 2, '(?<=\s)ied': 3, '(?<=\s)vbied': 3}

kidnap_dict = {'(?<=\s)kidnap': 3, '(?<=\s)abduct': 3, 'held\s+hostage': 3, 'hostage': 2, '(?<=\s)disappear': 1}

robbery_dict = {'(?<=\s)stole(?=\s)': 2, '(?<=\s)steal': 2, '(?<=\s)robbery(?=\s)': 4, '(?<=\s)robbed(?=\s)': 4,
'(?<=\s)loot': 4, '(?<=\s)burglar': 3, '(?<=\s)burglary': 3, '(?<=\s)theif': 3, '(?<=\s)raider': 2, '(?<=\s)intruder': 2}

def score(text, dict):
    score = 0
    for pattern, scaler in dict.iteritems():
        match_count = len(re.findall(pattern, text, re.IGNORECASE | re.MULTILINE))
        score += match_count * scaler
    return score

def classify_inci(text):
    score_dict = {}
    score_dict['ARSON'] = score(text, arson_dict)
    score_dict['ATTACK'] = score(text, attack_dict)
    score_dict['BOMBING'] = score(text, bomb_dict)
    score_dict['KIDNAPPING'] = score(text, kidnap_dict)
    score_dict['ROBBERY'] = score(text, robbery_dict)
    return max(score_dict.iteritems(), key=operator.itemgetter(1))[0]
