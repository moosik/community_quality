# Prepare community files to run with CommunityQuality.java
# Runs CommuityQuality.java and collects the results
#
#
# How to run: makeCommunity.py filename whereToWriteOutput resultFileName
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
# resultFileName
# path/name of the file where the results should be written
#
# author: Vitalina Komashko, mbyr consulting, LLC





from support_modules import *
import sys


# This creates dictionary of communities for each clustering
results = make_community(sys.argv[1])
# Write the dictionary of dictionaries to a directory as separate files in a format
# used by CommunityQuality.java

write_dics(results[1], sys.argv[2])


# After the files were created we can run CommunityQuality.java

stats = community_quality_extract(sys.argv[2])

# Write the results to a file

write_stats2file(stats, sys.argv[3])
