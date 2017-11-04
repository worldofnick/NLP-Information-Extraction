import nltk, re, pprint

# First preprocess data
def preprocessing(document):

    # Split the document into sentences using sent segmenter
    sentences = nltk.sent_tokenize(document)

    # Sub-divide each sent into token using a tokenizer
    sentences = [nltk.word_tokenize(word) for word in sentences]

    # pos tagger on each sentence
    sentences = [nltk.pos_tag(word) for word in sentences]
    print sentences
    return sentences


# A subject of a sentence S is the noun phrase that is the child of S and the sibling of VP.
def get_subject(chunked_sentence_tree):
    print "FINDING SUBJECT"
    if type(chunked_sentence_tree[0]) is nltk.Tree:
        if chunked_sentence_tree[0].label() == 'CLAUSE':
            print "Subject: " + str(chunked_sentence_tree[0][0])
        elif type(chunked_sentence_tree[1]) is nltk.Tree:
            if chunked_sentence_tree[0].label() == 'NP' and (chunked_sentence_tree[1].label() == 'VP'):
                print "Subject: " + str(chunked_sentence_tree[0])
    else:
        print "No subject found"
    #
    # (chunked_sentence_tree[1].label() == 'ACTIVE_VP' or
    #  chunked_sentence_tree[1].label() == 'PASSIVE_VP' or chunked_sentence_tree[1].label() == 'UNKWOWN_VP')
# Next perform chuncking (NP, VP, PP)
# Build an NP-Chunker using the POS tags and a
# 'Chunk Grammar' = rules that indicate how sentences should be chunked.
def np_chunker(sentence):
    print "Sentence in chunker: " + str(sentence[0])
    # NP = optional determiner + 0 or more adj of any type + 1 or more nouns of any type
  #   np_chunk_grammar = r"""
  # INFINITIVE: {<TO><VB>}
  # NP: {<DT|PRP\$|PRP|\$|CD|JJ|VBN|VBG|NN.*>+}          # Chunk sequences of DT, JJ, NN
  # PP: {<IN><NP>|<TO><NP>}               # Chunk prepositions followed by NP
  # UNKNOWN_VP: {<VBZ><VBN>|<VBP><VBN>|<VBD><VBN>}   # Can be either active or passive. Need to check aux verb
  # ACTIVE_VP: {<MD><VB><VBN><VBG>|<VBP><VBN><VBG>|<VBZ><VBN><VBG>|<VBD><VBN><VBG>|<MD><VB><VBG>|<MD><VB><VBN>|<VBZ><VBG>|<VBP><VBG>|<VBD><VBG>|<MD><VB>|<VBP>|<VBD>|<VBZ>} # Chunk Active Voice VP
  # PASSIVE_VP: {<MD><VB><VBN><VBN>|<MD><VB><VBN>|<VBZ><VBG><VBN>|<VBP><VBG><VBN>|<VBZ><VBN><VBN>|<VBP><VBN><VBN>|<VBD><VBG><VBN>|<VBD><VBN><VBN>} # Chunk Passive Voice VP
  # VP: {<UNKNOWN_VP|ACTIVE_VP|PASSIVE_VP><INFINITIVE|NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
  # CLAUSE: {<NP><VP>}           # Chunk NP, VP
  # """      #TODO: refine the tag pattern grammar
    np_chunk_grammar = r"""
    NP: {<DT|WP|PRP\$|PRP|\$|CD|JJ|VBG|CONJ|NN.*>+<PP>*}          # Chunk sequences of DT, JJ, NN
    PP: {<IN><NP>|<TO><NP>}               # Chunk prepositions followed by NP
    
    ADV: {<RB.*>*}
    CONJ: {<\,>*<CC>*<WDT>*<\,>*}
    AUX: {<MD>*}
    VP: {<VB.*>+<NP>*<PP>*<ADV>*}
    VP: {<VP>+<CONJ>+<VP>+}
    S: {<NP>+<AUX>*<VP>+}
    #S: {<S>+<CONJ><S>+}
    """  # TODO: refine the tag pattern grammar

#    PP: {<PP>+<CONJ><PP>+}

    chunk_parser = nltk.RegexpParser(np_chunk_grammar, loop=20)  #TODO: if dont want deeper structure, remove cascading loop argument
    result = chunk_parser.parse(sentence[0])    #TODO: embed in loop to chunk each sentence[i]
    print str(result)
    result.draw()       # TODO: Keep or remove. Draws a graph!
    t = nltk.Tree.fromstring(str(result))   # turn the chunked string to nltk tree
    get_subject(t)



def tree():
    tree1 = nltk.Tree('NP', ['Alice'])
    tree2 = nltk.Tree('NP', ['the', 'rabbit'])
    tree3 = nltk.Tree('VP', ['chased', tree2])
    tree4 = nltk.Tree('S', [tree1, tree3])

    for i in range(0, len(tree4)):
        print str(i) + ": " + str(tree4[i])
    # print

    # print
    # print tree4[1]
    # print

# document = u'the little yellow dog barked at the cat when the cat hissed at the dog'
document = u'the little yellow dog, rat was killing the cat'
# document = u'Two fish stores closed last week for repairs for christmas break'
# document = u'He sang a song in the shower badly'
# document = u'The dog, cat, rabbit and the tiger will eat the bone'
# document = u'I bought a book, but I returned it'
# document = u'They think he is mine to control'
# document = u'Rapunzel let down her long golden hair'
# document = u'The stolen goods are mine'
# document = u'the anticommunist action alliance reports the following to the honduran people, in particular, and to the international community in general'
# document = u'six people were killed and five wounded today in a bomb attack'
# document = u'six people were killed and five wounded today in a bomb attack that destroyed a peasant home in the town of quinchia, about 300 km west of bogota, in the coffee-growing department of risaralda, quinchia mayor saul botero has reported.'
tree()


print "--------------------------------------"
print "Preprocessed sentence: "
sentences = preprocessing(document)
print "--------------------------------------"
print
print "NP chunking"
np_chunker(sentences)
print "--------------------------------------"


