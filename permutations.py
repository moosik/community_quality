# Import modules

from support_modules import *
import random


# Calls make_community to create original community files
# Performs one round of shuffling, writes shuffled communities to files
def permute_dics(input_file, shuffle_dir):
    # Create a result_dir
    make_sure_path_exists(shuffle_dir)
    # Get the community dictionaries
    node_id, community_dictionary = make_community(input_file)
    # Set up empty dictionary to store the permuted results
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
            shuffled_sub_dic[sub_dic_key].extend(random_nodes[start_list_pos: (start_list_pos + list_len)])
            # change start_list_pos to advance through the list of random_nodes
            start_list_pos = start_list_pos + list_len
        # Add the new shuffled subdictionary to the large dictionary container of all of them
        permuted_dictionary[large_dic_key] = shuffled_sub_dic
    # Write the resulting shuffled dictionaries to files in the directory with all shuffled results
    write_dics(permuted_dictionary, shuffle_dir, shuffled=True)
    return permuted_dictionary


def dir_loop(input_file, shuffle_dir):
    loop_results = []
    for i in range(0, 5):
        random.seed(i)
        permute_dics(input_file, shuffle_dir)
        loop_results.append(community_quality_extract(shuffle_dir))
    return loop_results


temp = dir_loop("data/rosmap_test_train.txt", "shuffle_test1")


