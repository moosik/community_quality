# Import modules

from support_modules import *
import random


# Calls make_community to create original community files
# Performs one round of shuffling, writes shuffled communities to files
def permute_dics(input_file, shuffle_dir):
    # Create a result_dir
    make_sure_path_exists(shuffle_dir)
    f = open(input_file, 'r')
    # get the header
    header = f.readline()
    # Get community names and create empty community dictionary for all columns in the input file:
    com_names, empty_community_dic = create_community_dictionary(header, "\t")
    # Read the rest of the file into list of lists. Each list is a column of the input file:
    file_list = read_file2lists(f, header)
    # Now we need to shuffle the sublists (except the first sublist with the list of nodes)
    for item in range(1, len(file_list)):
        random.shuffle(file_list[item])
    # Next split to a dictionary of dictionaries
    node, permuted_dictionary = split2dics(file_list, com_names, empty_community_dic)
    # Write the shuffled dictionary to files
    write_dics(permuted_dictionary, shuffle_dir, shuffled=True)


## Loop to create random permutations and process the results for each
def dir_loop(input_file, shuffle_dir):
    loop_results = []
    for i in range(0, 5):
        random.seed(i)
        permute_dics(input_file, shuffle_dir)
        loop_results.append(community_quality_extract(shuffle_dir))
    return loop_results


#### Transform the obtain results into a dictionary of dictionaries
def perm_results2files(loop_results):
    statistics = ["VI", "NMI", "F", "NVD", "RI", "ARI", "JI"]
    # loop_results[0][0] give the list of pairs of files being compared
    for i in range(0, len(loop_results[0][0])):
        # Create an empty dictionary to store the results
        perm_results = dict()
        for el in range(len(statistics)):
            perm_results[statistics[el]] = []
        # Write the results of all permutations into corresponding lists for each statistic
        perm_results["VI"].extend([item[1][i] for item in loop_results])
        perm_results["NMI"].extend([item[2][i] for item in loop_results])
        perm_results["F"].extend([item[3][i] for item in loop_results])
        perm_results["NVD"].extend([item[4][i] for item in loop_results])
        perm_results["RI"].extend([item[5][i] for item in loop_results])
        perm_results["ARI"].extend([item[6][i] for item in loop_results])
        perm_results["JI"].extend([item[7][i] for item in loop_results])
        # Write the dictionary of dictionaries to a file in a wide format
        # where the first element is the name of the statistic and the rest
        # are the tab delimited results of the permutations
        result_file = open(loop_results[0][0][i], "w")
        for key in perm_results:
            # convert numbers to strings so they can be written to a file
            line2write = (str(w) for w in perm_results[key])
            result_file.write(key + "\t" + "\t".join(line2write) + "\n")
        result_file.close()







temp = dir_loop("data/rosmap_test_train.txt", "shuffle_test1")
perm_results2files(temp)


