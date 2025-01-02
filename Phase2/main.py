import json
import nltk
import spacy
import string
import os

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from autocorrect import Speller
from math import sqrt

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
            loweredQuote = quote.lower()

            # Remove all punctuation from the quote.
            cleanedQuote = loweredQuote.translate(str.maketrans("", "", string.punctuation))

            # Replace double spaces, with one space.
            singleSpacedQuote = cleanedQuote.replace("  ", " ")

            # Split quote, into individual words.
            tokenizedQuote = word_tokenize(singleSpacedQuote)

            # Remove stopwords and lemmatize the quote.
            lemmatizedQuote = [wordLemmatizer.lemmatize(token) for token in tokenizedQuote
                               if token not in stopWords and len(token) > 3]

            # Remove any spelling mistakes.
            correctQuote = [speller(value) for value in lemmatizedQuote]

            # Now we save the final tokenized quote
            # into the new dictionary structure.
            newQuoteList[key] = {
                "quote": correctQuote,
                "author": value["author"]
            }

        # Now we need to evaluate the total
        # quote characters per file, to clean
        # each dataset, from outliers.
        totalQuoteCharacters = 0
        for key, value in newQuoteList.items():

            quote = value["quote"]

            # Reconstruct the quote.
            reconstructedQuote = ''.join(token for token in quote)

            # Calculate its character length.
            characterLength = len(reconstructedQuote)

            # Add the length, to the total sum.
            totalQuoteCharacters += characterLength

        # Now we find the average
        # length per quote.
        totalQuotes = len(newQuoteList)
        avgCharLenPerQuote = totalQuoteCharacters / totalQuotes

        # Define the character length range
        # for the quote cleaning process
        # of the file.
        n = avgCharLenPerQuote / sqrt(2)
        lowerBound = avgCharLenPerQuote - n
        upperBound = avgCharLenPerQuote + n

        # We copy the dictionary, to avoid
        # conflicts, when deleting outliers.
        copyDictionary = newQuoteList.copy()
        for key, value in newQuoteList.items():

            quote = value["quote"]

            reconstructedQuote = ''.join(token for token in quote)
            characterLength = len(reconstructedQuote)

            smallerThanMin = (characterLength < lowerBound)
            biggerThanMax = (characterLength > upperBound)
            quoteIsOutOfBounds = (smallerThanMin or biggerThanMax)
            if quoteIsOutOfBounds: del copyDictionary[str(key)]

        # Now we build up the final dictionary
        # by assigning the correct keys, to
        # the cleaned dataset.
        newKey = 1
        newQuoteList.clear()
        for key, value in copyDictionary.items():

            newQuoteList[newKey] = {
                "quote": value["quote"],
                "author": value["author"]
            }

            newKey += 1

        # Finally, we save the dictionary to
        # a JSON file, for later processing
        # purposes.
        outputFolder = "Dataset/PData/"
        filename = "Author" + str(fileId) + ".json"
        joinedPath = os.path.join(outputFolder, filename)

        jsonData = json.dumps(newQuoteList, indent = 4)
        with open(joinedPath, 'w') as jsonFile:
            jsonFile.write(jsonData)

        fileId += 1
