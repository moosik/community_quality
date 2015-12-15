# Import modules

from support_modules import *
import random
from pushbullet import Pushbullet


# Calls make_community to create original community files
# Performs one round of shuffling, writes shuffled communities to files
def permute_dics(input_file, shuffle_dir):
    # Create a result_dir
    # make_sure_path_exists(shuffle_dir)
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
    write_dics(permuted_dictionary, shuffle_dir)


## Loop to create random permutations and process the results for each
def dir_loop(input_file, shuffle_dir):
    # Create an empty dictionary to collect the shuffled results
    all_shuffle = dict()
    for i in range(0, 5):
        random.seed()
        permute_dics(input_file, shuffle_dir)
        shuffle_res = community_quality_extract(shuffle_dir)
        for key in shuffle_res.keys():
            if key not in all_shuffle.keys():
                all_shuffle.setdefault(key, [shuffle_res[key]])
            else:
                all_shuffle[key].append(shuffle_res[key])
    return all_shuffle


# function to be used with multiple workers
# x will be passed to workers
def dirs_loop(x):
    # Create directory name
    shuffle_dir_name = "shuffle_test" + str(x)
    temp = dir_loop("data/rosmap_test_train.txt", shuffle_dir_name)
    write_permuted_stats2files(temp, shuffle_dir_name)
    pb.push_note("Permutations", "finished working on the directory %d"%(x))




from multiprocessing import Pool
pb = Pushbullet(return_push_api_key())

if __name__ == '__main__':
    p = Pool(2)
    p.map(dirs_loop, [1, 2, 3])


#temp = dir_loop("data/rosmap_test_train.txt", "shuffle_test1")
#write_permuted_stats2files(temp, "shuffle_test1")






