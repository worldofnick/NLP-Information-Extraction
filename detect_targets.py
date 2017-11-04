from __future__ import unicode_literals
import spacy
import nltk, re, pprint
from spacy.en import English

#TODO: change these common rules (<VBZ><VBN>|<VBP><VBN>|<VBD><VBN>) to corresponding was, were, had, etc
def is_passive(tagged_sentence):
    passive_tags = ['VBZ VBN', 'VBP VBN',
                    'VBZ VBG VBN', 'VBP VBG VBN',
                    'VBZ VBN VBN', 'VBP VBN VBN',
                    'VBD VBN',
                    'VBD VBG VBN',
                    'VBD VBN VBN',
                    'MD VB VBN',
                    'MD VB VBN VBN']

    # print u'========== PASSIVE TAGS =========='
    for tag in passive_tags:
        # print tag
        if tag in tagged_sentence:
            # print u'=========================='
            return True

    # print u'=========================='
    return False

def detect_targets(article_text, killing_words):
    titlecase_article_text = article_text.lower()
    # nlp = English()
    # doc = nlp(article_text)

    tokenized_sents = nltk.sent_tokenize(titlecase_article_text)
    targets = []
    en_nlp = English()


    # Process each sentence in the article
    for tokenized_sentence in tokenized_sents:
        pos_tags = []
        tags = []
        current_sentence = []
        doc = en_nlp(tokenized_sentence)
        nlp_sentence = next(doc.sents)

        # For each word in the tokenized sentences
        for i in range(0, nlp_sentence.end):
            np = nlp_sentence[i]
            pos_tags.append(np.tag_)
            tags.append(np.pos_)
            current_sentence.append(np.text)

        pos_tag_string = ' '.join(pos_tags)
        tag_string = ' '.join(tags)
        current_sent_str = ' '.join(current_sentence)
        isPassive = is_passive(pos_tag_string)
        isPreposition = False
        isInfinitive = False
        word_pos_tuples = zip(current_sentence, tags)


        print u'POS tag string  : ' + pos_tag_string
        print u'POS     string  : ' + tag_string
        print "Sentence        : " + current_sent_str
        print "is Passive voice : " + str(isPassive)

        if "ADP" in tag_string:
            isPreposition = True
        print "Is Preposition  : " + str(isPreposition)
        print

        if "TO" in pos_tag_string:
            isInfinitive = True
        print "Is Infinitive  : " + str(isInfinitive)
        print

        # active-vp prep <np> : <target>
        if not isPassive and isPreposition and not isInfinitive:
            prep_index = -1

            # for tuple in word_pos_tuples:
                # print str(tuple)


            for i in range(0, len(word_pos_tuples)):
                tuple = word_pos_tuples[i]
                if tuple[1] == 'ADP' and prep_index == -1:
                    # check if prev_word is in killing_words
                    np_prev = nlp_sentence[i-1]
                    if str(nlp_sentence[i - 1].lemma_).upper() not in killing_words:
                        prep_index = i
                        break

                if (tuple[1] == 'NOUN' or tuple[1] == 'PROPN') and prep_index != -1:
                    print "Target: " + str(tuple[0]).upper()
                    targets.append(str(tuple[0]).upper())
                elif tuple[1] == 'ADJ' and prep_index != -1:
                    compound_target_name = str(tuple[0])
                    for j in range(i+1, len(word_pos_tuples)):
                        t = word_pos_tuples[j]
                        if t[1] == 'NOUN' or t[1] == 'PROPN' or t[1] == 'ADJ':
                            if word_pos_tuples[j - 1][1] == 'PUNCT' and word_pos_tuples[j-1][0] != '.':
                                compound_target_name = compound_target_name + str(t[0])
                            else:
                                compound_target_name = compound_target_name + " " + str(t[0])
                        elif t[1] == 'PART' or (t[1] == 'PUNCT' and t[0] != '.'):
                            compound_target_name = compound_target_name + str(t[0])
                        elif t[1] == 'CCONJ':
                            j = j + 1
                        else:
                            i = j+1
                            break
                    print "Target: " + compound_target_name.upper()
                    targets.append(compound_target_name.upper())
                    break

            print "-----------------------------"

        elif not isPassive and not isInfinitive:
            print
            for i in range(0, len(word_pos_tuples)):
                tuple = word_pos_tuples[i]
                if tuple[1] == 'VERB' and str(nlp_sentence[i].lemma_).upper() in killing_words:
                    compound_target_name = ""
                    for j in range(i + 1, len(word_pos_tuples)):
                        t = word_pos_tuples[j]
                        if t[1] == 'NOUN' or t[1] == 'PROPN' or t[1] == 'ADJ':
                            compound_target_name = compound_target_name + " " + str(t[0])
                        elif t[1] == 'PART':
                            compound_target_name = compound_target_name + str(t[0])
                        elif t[1] == 'PRON':
                            if word_pos_tuples[j+1][1] == 'NOUN' or word_pos_tuples[j+1][1] == 'PROPN':
                                if word_pos_tuples[j - 1][1] == 'PUNCT' and word_pos_tuples[j-1][0] != '.':
                                    compound_target_name = compound_target_name + str(t[0])
                                else:
                                    compound_target_name = compound_target_name + " " + str(t[0])
                            elif t[1] == 'PART' or (t[1] == 'PUNCT' and t[0] != '.'):
                                compound_target_name = compound_target_name + str(t[0])
                        elif t[1] == 'CCONJ' or t[1] == 'DET':
                            j = j + 1
                        else:
                            i = j+1
                            break
                    print "Target: " + compound_target_name.upper()
                    targets.append(compound_target_name.upper())
                    break

        elif isPassive and not isInfinitive:
            subject_end_index = -1;
            for i in range(0, len(word_pos_tuples)):
                tuple = word_pos_tuples[i]
                if tuple[1] == 'VERB' and str(nlp_sentence[i].lemma_).upper() in killing_words:
                    subject_end_index = i
                    break

            for i in range(0, subject_end_index):
                tuple = word_pos_tuples[i]

                if tuple[1] == 'DET':
                    continue
                elif tuple[1] == 'ADJ' or tuple[1] == 'NOUN' or tuple[1] == 'PROPN':
                    compound_target_name = str(tuple[0])
                    for j in range(i + 1, subject_end_index):
                        t = word_pos_tuples[j]
                        if t[1] == 'NOUN' or t[1] == 'PROPN' or t[1] == 'ADJ':
                            if word_pos_tuples[j - 1][1] == 'PUNCT' and word_pos_tuples[j-1][0] != '.':
                                compound_target_name = compound_target_name + str(t[0])
                            else:
                                compound_target_name = compound_target_name + " " + str(t[0])
                        elif t[1] == 'PART' or (t[1] == 'PUNCT' and t[0] != '.'):
                            compound_target_name = compound_target_name + str(t[0])
                        elif t[1] == 'CCONJ':
                            j = j + 1
                        else:
                            i = j + 1
                            break
                    print "Target: " + compound_target_name.upper()
                    targets.append(compound_target_name.upper())
                    break




