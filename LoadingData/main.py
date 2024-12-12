import json as js

# Read the Quotes.txt file.
fileName = "Dataset/Quotes.txt"
with open(fileName, "r", encoding = "utf-8") as initialFile:

    content = initialFile.readlines()
    content = content[1: len(content) - 1]

# Convert the file's content, into
# its JSON counterpart.
data = {}
for k in range(len(content)):

    quote = content[k].strip('\n').replace('",', "")
    quote = quote.replace('"', "")
    data[k] = quote

# Save the new dictionary into a
# separate file, called Quotes.json.
jsonData = js.dumps(data, indent = 4)

with open('Dataset/Quotes.json', 'w') as jsonFile:
    jsonFile.write(jsonData)
