======================================================================
TESTED ON CADE, Lab 1, Machine #19
======================================================================

How to test?
----------------------------------------------------------------------
1. Change directory (cd) to the current 
unzipped location

1.1 Make sure to give proper permissions: chmod +x infoextract

2. Run "./infoextract <input-file-location>"

3. Score by "perl score-ie.pl AGGREGATE.templates developset/answers/AGGREGATE"
======================================================================

A) Resources

NLTK Used for tokenization: (http://www.nltk.org)
SpaCy Used for NER: (https://spacy.io)
Truecaser: Used to convert uppercase text to correctly cased text ** NOT CURRENTLY USED (https://github.com/nreimers/truecaser)
----------------------------------------------------------------------

B) Time Per Article

The program can process the entire developer/texts in under a minute on a MacBook Pro.
----------------------------------------------------------------------

C) Contributions

Nick Porter:
File I/O, Data Pipeline, CADE Script
Text Case Correction
Incident Classification
Weapon Detection
Organization Detection
Victim Detection

Snehashish Mishra:
Data Pipeline
Organization Detection
Victim Detection
Perp Individual Detection
Target Detection
----------------------------------------------------------------------

D) Limitations

Runs pretty fast but detection on some of the categories isn’t very good. Needs a better chunker and a sequence tagger (currently developing). The NER system for organization needs improvement.