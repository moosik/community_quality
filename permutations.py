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



def dir_loop(input_file, shuffle_dir):
    loop_results = []
    for i in range(0, 5):
        random.seed(i)
        permute_dics(input_file, shuffle_dir)
        loop_results.append(community_quality_extract(shuffle_dir))
    return loop_results


temp = dir_loop("data/rosmap_test_train.txt", "shuffle_test1")


