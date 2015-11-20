# Open provided file

f = open(filename, "r")

# Read the header to determine how many communities need to be created

header = f.readline()

# Remove the end of the line character from header

header = header.strip("\n")

# Obtain names of the communities from the header

headerFields = header.split("\t")
communityNames = headerFields[1:(len(headerFields)+1)]

# Create as many dictionaries as many community names we obtained:

communityDictionary = dict()

# Each element will also be a dictionary

for el in range(len(communityNames)):
    communityDictionary[communityNames[el]] = dict()


# For each line of the file we will add a unique element to each dictionary of the communities

# initiate line counter = unique node id

nodeID = 1

for lines in f.readlines():
    # some line fixing: remove \n, split by tab
    singleLine = lines.strip("\n")
    singleLineFields = singleLine.split("\t")
    for el in range(len(communityNames)):
        if communityDictionary[communityNames[el]].has_key(singleLineFields[el + 1]):
            communityDictionary[communityNames[el]][singleLineFields[el + 1]].append(nodeID)
        else:
            communityDictionary[communityNames[el]][singleLineFields[el + 1]] = [nodeID]
    # Advance line counter
    nodeID = nodeID + 1



# Write the dictionary contents into community files ready for processing
for key in communityDictionary.keys():
    communityFile = open(key, "w")
    for subkey in communityDictionary[key].keys():
        line2write = (str(w) for w in communityDictionary[key][subkey])
        communityFile.write(" ".join(line2write) + "\n")
    communityFile.close()
