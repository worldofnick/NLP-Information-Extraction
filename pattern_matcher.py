import nltk, re, pprint 

def preprocessing(document):

    # Split the document into sentences using sent segmenter
    sentences = nltk.sent_tokenize(document)

    # Sub-divide each sent into token using a tokenizer
    sentences = [nltk.word_tokenize(word) for word in sentences]

    # pos tagger on each sentence
    sentences = [nltk.pos_tag(word) for word in sentences]
    return sentences

def get_subject(chunked_sentence_tree):
    if type(chunked_sentence_tree[0]) is nltk.Tree:
        if chunked_sentence_tree[0].label() == 'S':
            return chunk_tree_to_sent(chunked_sentence_tree[0][0])
            # return str(chunked_sentence_tree[0][0])
    else:
        return '***'

punct_re = re.compile(r'\s([,\.;\?])')

def chunk_tree_to_sent(tree, concat=' '):
    words = []
    for tup in tree.leaves():
        words.append(tup.split('/')[0])

    s = concat.join(words)
    # s = concat.join([w for w, t in tree.leaves()]) 
    return re.sub(punct_re, r'\g<1>', s)


def np_chunker(sentence):
    np_chunk_grammar = r"""
    NP: {<DT|WP|PRP\$|PRP|\$|CD|JJ|NN.*>+<PP>*}          # Chunk sequences of DT, JJ, NN
    PP: {<IN><NP>|<TO><NP>}               # Chunk prepositions followed by NP
    NP: { < NP > + < CONJ > < ADV > * < NP > +}
    ADV: {<RB.*>*}
    CONJ: {<\,>*<CC>*<WDT>*<\,>*}
    AUX: {<MD>*}
    VP: {<VB.*>+<NP>*<PP>*<ADV>*}
    VP: { <VP>+<CONJ>+<VP>+}
    S: {<NP>+<AUX>*<VP>+}
    S: {<S>+<CONJ><S>+}

    """
    chunk_parser = nltk.RegexpParser(np_chunk_grammar, loop=20) 
    result = chunk_parser.parse(sentence)
    t = nltk.Tree.fromstring(str(result)) 

    return get_subject(t)

def find_victims(text):
    sentences = preprocessing(text.lower())
    victims = []
    
    
    for sentence in sentences:
        victim = np_chunker(sentence)
        if victim != '***' and victim != None:
            victims.append(victim)

    return victims


