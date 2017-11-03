pip install --user virtualenv

mkdir venv

python -m virtualenv venv

source venv/bin/activate

pip install spacy

python -m spacy download en

pip install --user nltk

python nltk_download.py

python main.py $1