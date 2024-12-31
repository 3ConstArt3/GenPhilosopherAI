import json
import nltk
import spacy
import string
import os

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from autocorrect import Speller

# Download specific nltk resources, that
# are necessary for the data preprocess step.
nltk.download('punkt_tab')
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

# Initialize a speller object, to get rid
# of any spelling mistake through the quotes.
speller = Speller(lang = "en")

# Initialize lemmatizer tools.
stopWords = set(stopwords.words("english"))
wordLemmatizer = WordNetLemmatizer()

fileId = 1
inputFolder = "Dataset/IData/"
for filename in os.listdir(inputFolder):

    if filename.endswith(".json"):

        philosopher = os.path.splitext(filename)[0]

        # Read the content of each file.
        joinedPath = os.path.join(inputFolder, filename)
        with open(joinedPath, "r", encoding = "utf-8") as jsonFile:
            quoteList = json.load(jsonFile)

        # Now we clean the quotes' dictionary,
        # from punctuation, or unnecessary stopwords.
        newQuoteList = dict()
        for key, value in quoteList.items():

            # Retrieve the quote.
            quote = value["quote"]

            # Convert each quote to lowercase.
            lowerQuote = quote.lower()

            # Remove all punctuation from the quote.
            cleanedQuote = lowerQuote.translate(str.maketrans("", "", string.punctuation))

            # Replace double spaces, with one space.
            singleSpacedQuote = cleanedQuote.replace("  ", " ")

            # Split quote, into individual words.
            tokens = word_tokenize(singleSpacedQuote)

            # Remove stopwords and lemmatize the quote.
            newValue = [wordLemmatizer.lemmatize(word) for word in tokens
                        if word not in stopWords and len(word) > 3]

            # Remove any spelling mistakes.
            correctValue = [speller(value) for value in newValue]

            # Now we save the final tokenized quote
            # into the new dictionary structure.
            newQuoteList[key] = {
                "quote": correctValue,
                "author": value["author"]
            }

        outputFolder = "Dataset/PData/"
        filename = "Author" + str(fileId) + ".json"
        joinedPath = os.path.join(outputFolder, filename)

        jsonData = json.dumps(newQuoteList, indent = 4)
        with open(joinedPath, 'w') as jsonFile:
            jsonFile.write(jsonData)

        fileId += 1
