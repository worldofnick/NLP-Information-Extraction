from __future__ import unicode_literals
import spacy
import nltk
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

def check_if_person(article_text, uppercase_perp_name, en_nlp):
    titled_prep = uppercase_perp_name.title()
    for ent in en_nlp(article_text.title()):
        if ent.text == titled_prep:
            if ent.ent_type_ == 'PERSON':  # TODO: add others? GPE, NORP, etc
                # print "Prep is person"
                return True
            else:
                return False
    return False

def detect_individuals(article_text, killing_words, en_nlp):
    # print "========= PREPS =============="
    titlecase_article_text = article_text.lower()
    # nlp = English()
    # doc = nlp(article_text)

    tokenized_sents = nltk.sent_tokenize(titlecase_article_text)
    perp_individuals = set()


    # Process each sentence in the article
    for tokenized_sentence in tokenized_sents:
        # print
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
        word_pos_tuples = zip(current_sentence, tags, pos_tags)

        # print u'POS tag string  : ' + pos_tag_string
        # print u'POS     string  : ' + tag_string
        # print "Sentence        : " + current_sent_str
        # print "is Passive voice : " + str(isPassive)

        if "ADP" in tag_string:
            isPreposition = True
        # print "Is Preposition  : " + str(isPreposition)

        if "TO" in pos_tag_string:
            isInfinitive = True
        # print "Is Infinitive  : " + str(isInfinitive)

        if isPassive and isInfinitive:
            subject_end_index = -1;
            for i in range(0, len(word_pos_tuples)):
                tuple = word_pos_tuples[i]
                if tuple[2] == 'TO' and str(nlp_sentence[i+1].lemma_).upper() in killing_words:
                    subject_end_index = i
                    break

            for i in range(0, subject_end_index):
                tuple = word_pos_tuples[i]

                if tuple[1] == 'DET':
                    continue
                elif tuple[1] == 'ADJ' or tuple[1] == 'NOUN' or tuple[1] == 'PROPN':
                    compound_perp_name = str(tuple[0])
                    for j in range(i + 1, subject_end_index):
                        t = word_pos_tuples[j]
                        if t[1] == 'NOUN' or t[1] == 'PROPN' or t[1] == 'ADJ':
                            if word_pos_tuples[j-1][1] == 'PUNCT' and word_pos_tuples[j-1][0] != '.':
                                compound_perp_name = compound_perp_name + str(t[0])
                            elif t[1] == 'ADJ':
                                compound_perp_name = compound_perp_name + " " + str(t[0])
                            else:
                                compound_perp_name = str(t[0])
                        elif t[1] == 'PART' or  (t[1] == 'PUNCT' and t[0] != '.'):
                            compound_perp_name = compound_perp_name + str(t[0])
                        elif t[1] == 'CCONJ':
                            j = j + 1
                            # Add the name before the conj to the list
                            if check_if_person(article_text.title(), compound_perp_name.upper(), en_nlp):
                                perp_individuals.add(compound_perp_name.upper())
                            compound_perp_name = ""
                        else:
                            i = j + 1
                            break
                    if compound_perp_name != "":
                        if check_if_person(article_text.title(), compound_perp_name.upper(), en_nlp):
                            perp_individuals.add(compound_perp_name.upper())
                        compound_perp_name = ""
                        break

                    # print "Found Preps to be verified: " + compound_perp_name.upper()

                    # titled_prep = compound_perp_name.title()
                    # for ent in en_nlp(article_text.title()):
                    #     if ent.text == titled_prep:
                    #         if ent.ent_type_ == 'ORG': #TODO: add others? GPE, NORP, etc
                    #             print "Prep is org"
                    #             perp_individuals.add(compound_perp_name.upper())
                    #             print
                    #         break
                    # break
            # print str(perp_individuals)
            # print

        elif isPassive and isPreposition and not isInfinitive:

            prep_index = -1

            for i in range(0, len(word_pos_tuples)):
                tuple = word_pos_tuples[i]
                if tuple[1] == 'ADP' and prep_index == -1:
                    # check if prev_word is in killing_words. If not, quit
                    np_prev = nlp_sentence[i - 1]
                    prep_index = i
                    if str(np_prev.lemma_).upper() not in killing_words:
                        break

                # if (tuple[1] == 'NOUN' or tuple[1] == 'PROPN') and prep_index != -1:
                #     print "Found prep to be checked: " + str(tuple[0]).upper()
                #     perp_orgs.append(str(tuple[0]).upper())
                # elif
                if (tuple[1] == 'ADJ' or tuple[1] == 'NOUN' or tuple[1] == 'PROPN') and prep_index != -1:
                    compound_perp_name = str(tuple[0])
                    for j in range(i + 1, len(word_pos_tuples)):
                        t = word_pos_tuples[j]
                        if t[1] == 'NOUN' or t[1] == 'PROPN' or t[1] == 'ADJ':
                            if word_pos_tuples[j - 1][1] == 'PUNCT' and word_pos_tuples[j-1][0] != '.':
                                compound_perp_name = compound_perp_name + str(t[0])
                            elif t[1] == 'ADJ':
                                compound_perp_name = compound_perp_name + " " + str(t[0])
                            else:
                                compound_perp_name = str(t[0])
                        elif t[1] == 'PART' or  (t[1] == 'PUNCT' and t[0] != '.'):
                            compound_perp_name = compound_perp_name + str(t[0])
                        elif t[1] == 'CCONJ':
                            j = j + 1
                            if check_if_person(article_text.title(), compound_perp_name.upper(), en_nlp):
                                perp_individuals.add(compound_perp_name.upper())
                            compound_perp_name = ""
                        else:
                            i = j + 1
                            break
                    if compound_perp_name != "":
                        if check_if_person(article_text.title(), compound_perp_name.upper(), en_nlp):
                            perp_individuals.add(compound_perp_name.upper())
                        compound_perp_name = ""
                        break
                    # print "Found prep to be checked: " + compound_target_name.upper()
                    # print
                    # titled_prep = compound_perp_name.title()
                    # for ent in en_nlp(article_text.title()):
                    #     if ent.text == titled_prep:
                    #         if ent.ent_type_ == 'ORG':  # TODO: add others? GPE, NORP, etc
                    #             print "Prep is org"
                    #             print
                    #             perp_orgs.append(compound_perp_name.upper())
                    #         break
                    # break
            # print str(perp_individuals)
            # print

        elif not isPassive and isInfinitive:
            subject_end_index = -1;
            for i in range(0, len(word_pos_tuples)):
                tuple = word_pos_tuples[i]
                if tuple[2] == 'TO' and str(nlp_sentence[i + 1].lemma_).upper() in killing_words:
                    subject_end_index = i
                    break

            for i in range(0, subject_end_index):
                tuple = word_pos_tuples[i]

                if tuple[1] == 'DET':
                    continue
                elif tuple[1] == 'ADJ' or tuple[1] == 'NOUN' or tuple[1] == 'PROPN':
                    compound_perp_name = str(tuple[0])
                    for j in range(i + 1, subject_end_index):
                        t = word_pos_tuples[j]
                        if t[1] == 'NOUN' or t[1] == 'PROPN' or t[1] == 'ADJ':
                            if word_pos_tuples[j - 1][1] == 'PUNCT' and word_pos_tuples[j - 1][0] != '.':
                                compound_perp_name = compound_perp_name + str(t[0])
                            elif t[1] == 'ADJ':
                                compound_perp_name = compound_perp_name + " " + str(t[0])
                            else:
                                compound_perp_name = str(t[0])
                        elif t[1] == 'PART' or (t[1] == 'PUNCT' and t[0] != '.'):
                            compound_perp_name = compound_perp_name + str(t[0])
                        elif t[1] == 'CCONJ':
                            j = j + 1
                            if check_if_person(article_text.title(), compound_perp_name.upper(), en_nlp):
                                perp_individuals.add(compound_perp_name.upper())
                            compound_perp_name = ""
                        else:
                            i = j + 1
                            break
                    if compound_perp_name != "":
                        if check_if_person(article_text.title(), compound_perp_name.upper(), en_nlp):
                            perp_individuals.add(compound_perp_name.upper())
                        compound_perp_name = ""
                        break
            # print str(perp_individuals)
            # print

        # ------------------- down
        elif not isPassive and not isInfinitive and not isPreposition:
            subject_end_index = -1;
            for i in range(0, len(word_pos_tuples)):
                lemma = str(nlp_sentence[i].lemma_).upper()
                if lemma in killing_words:
                    subject_end_index = i
                    break

            for i in range(0, subject_end_index):
                tuple = word_pos_tuples[i]

                if tuple[1] == 'DET':
                    continue
                elif tuple[1] == 'ADJ' or tuple[1] == 'NOUN' or tuple[1] == 'PROPN':
                    compound_perp_name = str(tuple[0])
                    for j in range(i + 1, subject_end_index):
                        t = word_pos_tuples[j]
                        if t[1] == 'NOUN' or t[1] == 'PROPN' or t[1] == 'ADJ':
                            if word_pos_tuples[j - 1][1] == 'PUNCT' and word_pos_tuples[j - 1][0] != '.':
                                compound_perp_name = compound_perp_name + str(t[0])
                            elif t[1] == 'ADJ':
                                compound_perp_name = compound_perp_name + " " + str(t[0])
                            else:
                                compound_perp_name = str(t[0])
                        elif t[1] == 'PART' or (t[1] == 'PUNCT' and t[0] != '.'):
                            compound_perp_name = compound_perp_name + str(t[0])
                        elif t[1] == 'CCONJ':
                            j = j + 1
                            if check_if_person(article_text.title(), compound_perp_name.upper(), en_nlp):
                                perp_individuals.add(compound_perp_name.upper())
                            compound_perp_name = ""
                        else:
                            i = j + 1
                            break
                    if compound_perp_name != "":
                        if check_if_person(article_text.title(), compound_perp_name.upper(), en_nlp):
                            perp_individuals.add(compound_perp_name.upper())
                        compound_perp_name = ""
                        break
            # print str(perp_individuals)
            # print



    # print "========= END =============="

    return perp_individuals






    # nlp = English()
    # doc = nlp(article_text)
    # orgs = []
    # for ent in doc.ents:
    #     if ent.label_ == 'ORG':
    #         orgs.append(ent.text)
    #
    # return orgs
