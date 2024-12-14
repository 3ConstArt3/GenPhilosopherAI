import json as js
import nltk
import string
import spacy

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load the data from Quotes.json file.
fileName = "Dataset/Quotes.json"
with open(fileName, mode = "r", encoding = "utf-8") as jsonFile:
    quoteDictionary = js.load(jsonFile)

# Download specific nltk resources, that
# are necessary for the data preprocess step.
nltk.download('punkt_tab')
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

# Initialize lemmatizer tools.
stopWords = set(stopwords.words("english"))
wordLemmatizer = WordNetLemmatizer()

# Preprocess the dictionary of quotes.
processedData = dict()
for key, value in quoteDictionary.items():

    # Convert each quote to lowercase.
    lowerQuote = value.lower()

    # Remove all punctuation from the quote.
    cleanedQuote = lowerQuote.translate(str.maketrans("", "", string.punctuation))

    # Replace double spaces, with one space.
    singleSpacedQuote = cleanedQuote.replace("  ", " ")

    # Split quote, into individual words.
    tokens = word_tokenize(singleSpacedQuote)

    # Remove stopwords and lemmatize the quote.
    newValue = [wordLemmatizer.lemmatize(word) for word in tokens
                        if word not in stopWords and len(word) > 2]

    processedData[key] = newValue

# In the following section, we are going
# to create 3 separate JSON files.
#
# The 1st is going to have only nouns, as
# tokens.
#
# The 2nd is going to have only verbs, as
# tokens.
#
# The 3rd is going to contain both of them.
onlyNouns = dict()
for key, value in processedData.items():

    newValue = [word for word in value
                if not nlp(word)[0].pos_ == "VERB"]
    onlyNouns[key] = newValue

onlyVerbs = dict()
for key, value in processedData.items():

    newValue = [word for word in value
                if nlp(word)[0].pos_ == "VERB"]
    onlyVerbs[key] = newValue

# And now we need to save these new dictionaries
# in separate JSON files, for more clarity.
jsonData = js.dumps(processedData, indent = 4)
with open('Dataset/VerbsAndNouns.json', 'w') as jsonFile:
    jsonFile.write(jsonData)

jsonData = js.dumps(onlyNouns, indent = 4)
with open('Dataset/OnlyNouns.json', 'w') as jsonFile:
    jsonFile.write(jsonData)

jsonData = js.dumps(onlyVerbs, indent = 4)
with open('Dataset/OnlyVerbs.json', 'w') as jsonFile:
    jsonFile.write(jsonData)
