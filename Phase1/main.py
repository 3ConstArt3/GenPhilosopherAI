import json as js
import os
import chardet

# Convert the content of the files
# into utf-8 format, to avoid unicode
# errors, in the process.
inputFolder = "Dataset/InitialData/"
for filename in os.listdir(inputFolder):

    if filename.endswith(".txt"):

        joinedPath = os.path.join(inputFolder, filename)
        with open(joinedPath, "rb") as file:

            rawData = file.read()
            encodingName = chardet.detect(rawData)['encoding']

        with open(joinedPath, "r", encoding = encodingName) as file:
            content = file.read()
        with open(joinedPath, "w", encoding = "utf-8") as file:
            file.write(content)

# Convert each file, to its JSON format,
# for readability and also for later
# convenience, when the data processing
# is deemed necessary for the AI model's
# training session.
for filename in os.listdir(inputFolder):

    if filename.endswith(".txt"):

        philosopher = os.path.splitext(filename)[0].lower()

        # Read the content of each file.
        joinedPath = os.path.join(inputFolder, filename)
        with open(joinedPath, "r", encoding="utf-8") as initialFile:
            quoteString = initialFile.readlines()

        # Convert the data to a JSON
        # dictionary data structure.
        data = {}
        for k in range(len(quoteString)):

            quote = quoteString[k].strip('\n')
            quote = quote.replace('"', "")
            data[k + 1] = {
                "quote": quote,
                "author": philosopher
            }

        # Now we save the newly created
        # dictionary in a separate file.
        jsonData = js.dumps(data, indent = 4)

        outputFolder = "Dataset/ProcessedData/"
        filename = philosopher[0].upper() + philosopher[1:] + ".json"
        joinedPath = os.path.join(outputFolder, filename)
        with open(joinedPath, 'w') as jsonFile:
            jsonFile.write(jsonData)
