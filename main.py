from Article import Article
import os


ARTICLE_LOCATION = 'developset/texts'

def main():
    for file_name in os.listdir(ARTICLE_LOCATION):
        text = open(os.path.join(os.path.dirname(__file__), ARTICLE_LOCATION + '/' + file_name)).readlines()
        article = Article(text)
        break
        # We can either store all articles, or process them in a streaming matter

        # extracted_info = extract(article)
        # Use ExtractedInfo.py to write to file


# def loadData(file_name):
# 	# Array of names
# 	X = []
#
# 	# Array of labels (+, -)
# 	Y = []
#
# 	for line in open(os.path.join(os.path.dirname(__file__), 'updated_test/' + file_name)):
# 		label = line[0]
# 		full_name = line[1: len(line) - 2].strip()
# 		X.append(featureize(full_name))
# 		Y.append(label)
#
# 	return X, Y


main()
