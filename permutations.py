
# Import modules
import sys

# Module definitions

# Check whether the path has back slash at the end and add it if doesn't have it
def fixPath(inputPath):
    if inputPath[len(inputPath) - 1] != '/':
        inputPath = inputPath + '/'
    return inputPath


# This module take the header line and creates dictionary of dictionaries to store community results
# The sting can be delimited by whatever character, however
def createCommunityDictionary(line, delim):
    # Remove end of the line character if it is present
    if line[len(line) - 1] != '\n':
        line = line.strip("\n")
    # Obtain names of the communities from the header
    lineFields = line.split(delim)
    communityNames = lineFields[1:(len(lineFields) + 1)]
    # Create as many dictionaries as many community names we obtained:
    communityDictionary = dict()
    # Each element will also be a dictionary
    for el in range(len(communityNames)):
        communityDictionary[communityNames[el]] = dict()
    return communityDictionary, communityNames


# Split the contents of the file into dictionaries
def split2dics(file, communityNames, communityDictionary):
    nodeID = 1
    for lines in file.readlines():
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
    return nodeID, communityDictionary


# Write the dictionary of dictionaries to files to create the final community files:
def writeDics(communityDictionary, path):
    for key in communityDictionary.keys():
        communityFile = open(path + key, "w")
        for subkey in communityDictionary[key].keys():
            line2write = (str(w) for w in communityDictionary[key][subkey])
            communityFile.write(" ".join(line2write) + "\n")
        communityFile.close()


# Wrapper function that uses all functions above to
# read the input file and create community files from the input file
# it returns the number of nodes (actual is -1) which were put into communities
# and the filled dictionary of dictionaries with the communities
def makeCommunity(inputFile, outputDirectory):
    f = open(inputFile, 'r')
    # fix the path format of the output directory by adding "/" if necessary
    outputDirectory = fixPath(outputDirectory)
    # get the header
    header = f.readline()
    # Get community names and create empty community dictionary for all columns in the input file:
    cNames, cDicEmpty = createCommunityDictionary(header, "\t")
    # Get the final node count, filled community dictionary
    node, cDic = split2dics(f, cNames, cDicEmpty)
    # Write the dictionaries into files:
    writeDics(cDic, outputDirectory)
    # close the input file
    f.close()
    return node, cDic


# Function to permute the dictionary contents
def permuteDictionary(inputDic):


# Create the original community files and return the dictionary of dictionaries with the node number

nodeID, dicDics = makeCommunity(sys.argv[1], sys.argv[2])


tempdic = dict()
for key in communityDictionary.keys():
