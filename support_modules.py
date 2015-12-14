import os.path
import subprocess
import errno


#######################################################################################
## Modules related to creating community files in preparation for running the java code

# Check if the directory already exists
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


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



# Function to read the entire input file into list of lists. Each element of the list
# will either have the list of nodes or the community ids. This will useful to set up
# independent permutations of each partition

def read_file2lists(input_file_handler, file_header):
    # Figure out how many sublists will be in a list
    header = file_header.strip("\n")
    header_fields = header.split("\t")
    communities_list = []
    # create a list of lists. number of sublists equal to the number
    # of elements in the header (the extra list is for storing the node ids)
    for i in range(0, len(header_fields)):
        communities_list.append([])
    # Next fill this empty list with node ids and the community ids:
    i = 1
    for lines in input_file_handler.readlines():
        single_line = lines.strip("\n")
        single_line_fields = single_line.split("\t")
        # add the node id as a counter
        communities_list[0].append(i)
        for j in range(1, len(single_line_fields)):
            communities_list[j].append(single_line_fields[j])
        i = i + 1
    return communities_list


# Split the contents of the file into dictionaries
# file_list is the output from read_file2lists: list of lists where every element contains a column from the file.
# the first column is the numeric sequence serving as node ids.
def split2dics(file_list, community_names, community_dictionary):
    # all lists in the file_list are of the same size, take the first one to
    # create and iteration
    for i in range(0, len(file_list[0])):
        for j in range(0, len(community_names)):
            if file_list[j + 1][i] in community_dictionary[community_names[j]]:
                community_dictionary[community_names[j]][file_list[j+1][i]].append(file_list[0][i])
            else:
                community_dictionary[community_names[j]][file_list[j+1][i]] = [file_list[0][i]]
    return i, community_dictionary



# Write the dictionary of dictionaries to files to create the final community files:
def write_dics(community_dictionary, path):
    path = fix_path(path)
    for key in community_dictionary.keys():
        community_file = open(path + key, "w")
        for subkey in community_dictionary[key].keys():
            line2write = (str(w) for w in community_dictionary[key][subkey])
            community_file.write(" ".join(line2write) + "\n")
        community_file.close()


# Function to create community files and write them to a file.
# Relies on all modules above. Returns the number of nodes (actual is -1) and
# the dictionary of dictionaries with the communities
def make_community(input_file):
    f = open(input_file, 'r')
    # get the header
    header = f.readline()
    # Get community names and create empty community dictionary for all columns in the input file:
    com_names, empty_community_dic = create_community_dictionary(header, "\t")
    # Read the rest of the file into list of lists. Each list is a column of the input file:
    file_list = read_file2lists(f, header)
    # Get the final node count, filled community dictionary
    node, community_dictionary = split2dics(file_list, com_names, empty_community_dic)
    # Write the dictionaries into files:
    # write_dics(community_dictionary, result_dir)
    # close the input file
    f.close()
    return node, community_dictionary









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


# Wrapping function to run CommunityQuality.java on all pairs of files found in the input_files_dir
def community_quality_extract(input_files_dir):
    files_to_process = os.listdir(input_files_dir)
    # vi = []
    # nmi = []
    # f_measure = []
    # nvd = []
    # ri = []
    # ari = []
    # ji = []
    # compared_pairs = []
    all_results = dict()
    # Loop to run each possible combinations of discovered and ground truth communities
    for i in range(0, len(files_to_process)):
        for j in range(i+1, len(files_to_process)):
            # Saved the names of the pair of files being compared
            # compared_pairs.append(files_to_process[i]+'-'+files_to_process[j])
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
            vi = extract_measures(stats_list, 0)
            nmi = extract_measures(stats_list, 1)
            f_measure = extract_measures(stats_list, 2)
            nvd = extract_measures(stats_list, 3)
            ri = extract_measures(stats_list, 4)
            ari = extract_measures(stats_list, 5)
            ji = extract_measures(stats_list, 6)
            all_results[files_to_process[i]+'-'+files_to_process[j]] = [vi, nmi, f_measure, nvd, ri, ari, ji]
    return all_results



# Module to write the statistics obtained from CommunityQuality.java to a file
def write_stats2file(results2write, output_file_name):
    # Open file to write the results of the computation
    f = open(output_file_name, "w")
    # Prepare the header, write to the output file
    result_header = ["Discovered Communities", "Ground Truth", "VI", "NMI", "F-measure", "NVD", "RI", "ARI", "JI"]
    result_header = "\t".join(result_header)
    end_line = "\n"
    f.write(result_header + end_line)
    # Get the length of the first element in results2write so we can loop through all of them
    # how_many = len(results2write[0])
    # Write the results to a file
    # for i in range(0, how_many):
    #     line2write = [item[i] for item in results2write]
    #     line2write = "\t".join(line2write)
    #     f.write(line2write + end_line)
    for key,value in results2write.items():
        f.write(key.replace("-", "\t") + "\t" + "\t".join([str(round(float(w), 4)) for w in value]) + end_line)
    f.close()



# Write the permuted results to file by appending them
def write_permuted_stats2files(results2write, shuffled_dir):
    shuffled_dir = fix_path(shuffled_dir)
    for key in results2write:
        f = open(shuffled_dir+key, "w")
        result_header = ["VI", "NMI", "F-measure", "NVD", "RI", "ARI", "JI"]
        result_header = "\t".join(result_header)
        end_line = "\n"
        f.write(result_header + end_line)
        for item in results2write[key]:
            f.write("\t".join([str(round(float(w), 4)) for w in item]) + end_line)
        f.close()

# Use Pushbullet to notify about the results
import json
import os.path

def return_push_api_key():
    with open(os.path.expanduser("~/.rpushbullet.json")) as data_file:
        data = json.load(data_file)
    return data["key"]

