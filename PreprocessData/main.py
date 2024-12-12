import json as js
import nltk
import string

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

# Save the new processed data into a
# separate file, called ProcessedData.json.
jsonData = js.dumps(processedData, indent = 4)

with open('Dataset/ProcessedData.json', 'w') as jsonFile:
    jsonFile.write(jsonData)
