# Prepare community files to run with CommunityQuality.java
#
#
# How to run: makeCommunity.py filename whereToWriteOutput
#
#
# Description of input parameters:
#
# filename:
# a tab separated file with at least two columns:
# column 1 - node ids. Format is irrelevant, however ids must be unique.
# At this point the function doesn't check for uniqueness.
# column 2 (and other if present) - cluster membership for each node
# The file is expected to have meaningful header because the community
# files will be saved under the header line corresponding to each cluster
# column. The script will work with any number of cluster membership columns.
#
# whereToWriteOutput: path to a directory where the resulting community
# files will be saved
#
#
# author: Vitalina Komashko, mbyr consulting, LLC
#


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
    if line[len(line) - 1] == '\n':
        line = line.strip("\n")
    # Obtain names of the communities from the header
    lineFields = line.split(delim)
    communityNames = lineFields[1:(len(lineFields) + 1)]
    # Create as many dictionaries as many community names we obtained:
    communityDictionary = dict()
    # Each element will also be a dictionary
    for el in range(len(communityNames)):
        communityDictionary[communityNames[el]] = dict()
    return communityNames, communityDictionary


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


makeCommunity(sys.argv[1], sys.argv[2])



