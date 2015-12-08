
# Import modules

import random
import sys
import os.path, subprocess


# Module definitions

#######################################################################################
## Modules related to creating community files in preparation for running the java code

# Check whether the path has back slash at the end and add it if doesn't have it
def fix_path(path):
    if path[len(path) - 1] != '/':
        path += '/'
    return path


# This module takes the header line in a file and creates dictionary of dictionaries to store communities
def create_community_dictionary(line, delim):
    # Remove end of the line character if it is present
    if line[len(line) - 1] == '\n':
        line = line.strip("\n")
    # Obtain names of the communities from the header
    line_fields = line.split(delim)
    community_names = line_fields[1:(len(line_fields) + 1)]
    # Create as many dictionaries as many community names we obtained:
    community_dictionary = dict()
    # Each element will also be a dictionary
    for el in range(len(community_names)):
        community_dictionary[community_names[el]] = dict()
    return community_names, community_dictionary


# Split the contents of the file into dictionaries
def split2dics(f, community_names, community_dictionary):
    node_id = 1
    for lines in f.readlines():
        # some line fixing: remove \n, split by tab
        single_line = lines.strip("\n")
        single_line_fields = single_line.split("\t")
        for el in range(len(community_names)):
            if single_line_fields[el + 1] in community_dictionary[community_names[el]]:
                community_dictionary[community_names[el]][single_line_fields[el + 1]].append(node_id)
            else:
                community_dictionary[community_names[el]][single_line_fields[el + 1]] = [node_id]
        # Advance line counter
        node_id = node_id + 1
    return node_id, community_dictionary


# Write the dictionary of dictionaries to files to create the final community files:
def write_dics(community_dictionary, path, shuffled=False):
    path = fix_path(path)
    for key in community_dictionary.keys():
        if shuffled:
            community_file = open(path + key + "_" + "permuted", "w")
            for subkey in community_dictionary[key].keys():
                line2write = (str(w) for w in community_dictionary[key][subkey])
                community_file.write(" ".join(line2write) + "\n")
            community_file.close()
        else:
            community_file = open(path + key, "w")
            for subkey in community_dictionary[key].keys():
                line2write = (str(w) for w in community_dictionary[key][subkey])
                community_file.write(" ".join(line2write) + "\n")
            community_file.close()



# Function to create community files and write them to a file.
# Relies on all modules above. Returns the number of nodes (actual is -1) and
# the dictionary of dictionaries with the communities
def make_community(input_file, result_dir):
    f = open(input_file, 'r')
    # get the header
    header = f.readline()
    # Get community names and create empty community dictionary for all columns in the input file:
    com_names, empty_community_dic = create_community_dictionary(header, "\t")
    # Get the final node count, filled community dictionary
    node, community_dictionary = split2dics(f, com_names, empty_community_dic)
    # Write the dictionaries into files:
    write_dics(community_dictionary, result_dir)
    # close the input file
    f.close()
    return node, community_dictionary


# Calls make_community to create original community files
# Performs one round of shuffling, writes shuffled communities to files
def permute_dics(input_file, result_dir, shuffle_dir):
    node_id, community_dictionary = make_community(input_file, result_dir)
    permuted_dictionary = dict()
    # Shuffle the list only once for all dictionaries
    random_nodes = range(1, node_id)
    random.shuffle(random_nodes)
    for large_dic_key in community_dictionary:
        sub_dic = community_dictionary[large_dic_key]
        # Create an empty dictionary like tempDic, which will hold shuffled elements
        shuffled_sub_dic = dict()
        for sub_dic_key in sub_dic:
            shuffled_sub_dic[sub_dic_key] = []
        # Fill the shuffledDict with the elements of the list of nodes. Each dictionary value will be
        # a list and it will have the same length as in the original dictionary
        start_list_pos = 0
        for sub_dic_key in sub_dic:
            list_len = len(sub_dic[sub_dic_key])
            shuffled_sub_dic[sub_dic_key].extend(random_nodes[start_list_pos : (start_list_pos + list_len)])
            # change start_list_pos to advance through the list of random_nodes
            start_list_pos = start_list_pos + list_len
        # Add the new shuffled subdictionary to the large dictionary container of all of them
        permuted_dictionary[large_dic_key] = shuffled_sub_dic
    # Write the resulting shuffled dictionaries to files in the directory with all shuffled results
    write_dics(permuted_dictionary, shuffle_dir, shuffled=True)
    return permuted_dictionary, community_dictionary


######################################################################################
## Modules related to running the java code CommunityQuality.java and processing
## its results

# Execute compiled java with given files
def execute_java(java_file, discovered_comm, ground_truth):
    java_class, ext = os.path.splitext(java_file)
    cmd = ['java', java_class, discovered_comm, ground_truth]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


# Extract values for each statistic
def extract_measures(input_list, el):
    measure = input_list[el]
    measure_num = measure.split(" = ")[1]
    return measure_num

def loop_through_files(input_files_dir, output_file):
    #dir_with_files = sys.argv[1]
    #output_file = open(sys.argv[2], "w")

    files_to_process = os.listdir(input_files_dir)
    # Open file to write the results of the computation
    f = open(output_file, "w")
    # Prepare the header, write to the output file
    result_header = ["Discovered Communities", "Ground Truth", "VI", "NMI", "F-measure", "NVD", "RI", "ARI", "JI"]
    result_header = "\t".join(result_header)
    end_line = "\n"
    f.write(result_header + end_line)
    # Loop to run each possible combinations of discovered and ground truth communities
    for i in range(0, len(files_to_process)):
        for j in range(0, len(files_to_process)):
            # Run CommunityQuality
            java_run_out = execute_java('CommunityQuality.java', os.path.join(input_files_dir, files_to_process[i]), os.path.join(input_files_dir, files_to_process[j]))

            # Process the obtained results
            # Obtain the string - result of the command substitution
            stats_string = java_run_out.stdout.read()

            # Substitute the first 2 '\n' with ', '
            stats_string = stats_string.replace("\n", ", ", 2)

            # Remove '\n' at the end of the string:
            stats_string = stats_string.replace("\n", "")

            # Split the string into a list by ', '
            stats_list = stats_string.split(", ")

            # Extract the statistics
            VI = extract_measures(stats_list, 0)
            NMI = extract_measures(stats_list, 1)
            F = extract_measures(stats_list, 2)
            NVD = extract_measures(stats_list, 3)
            RI = extract_measures(stats_list, 4)
            ARI = extract_measures(stats_list, 5)
            JI = extract_measures(stats_list, 6)

            # Write the result of the comparison to the file, first 2 elements are the names of the files
            # being compared
            final_list = [files_to_process[i], files_to_process[j], VI, NMI, F, NVD, RI, ARI, JI]
            final_list = "\t".join(final_list)
            f.write(final_list +  end_line)
    f.close()



result = permute_dics("data/rosmap_test_train.txt", "results/results", "results/permuted")
# Do calculations on the non-permuted results
loop_through_files("results/results", "results/results/results.txt")
# Do calculations on the permuted results
loop_through_files("results/permuted", "results/permuted/permuted_results.txt")

