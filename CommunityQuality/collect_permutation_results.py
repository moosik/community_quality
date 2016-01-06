from support_modules import fix_path
import os
import os.path

def collect_permutation_results(dir):
    # get list of all files/directories in the dir
    dir_content = os.listdir(dir)
    # Select only directories that have "shuffle_test" in them
    shuffle_dir_list = [f for f in dir_content if "shuffle_test" in f and os.path.isdir(f)]
    # Write all results to a dictionary, initiate it
    all_permutations = dict()
    for d in shuffle_dir_list:
        d = fix_path(d)
        # Get the list of files
        dir_files = os.listdir(d)
        # Find all files which have the word answer in them
        dir_files_list = [f for f in dir_files if "answer_" in f]
        for i in range(0, len(dir_files_list)):
            f = open(d + dir_files_list[i], "r")
            header = f.readline()
            for line in f.readlines():
                all_permutations.setdefault(dir_files_list[i], []).append(line)
            f.close()
    return all_permutations

# Write the results to files
def write_permut2files(results2write):
    # Will write just to the current directory
    for key in results2write:
        f = open(key, "w")
        result_header = ["VI", "NMI", "F-measure", "NVD", "RI", "ARI", "JI"]
        f.write("\t".join(result_header) + "\n")
        for item in results2write[key]:
            f.write(item)
        f.close()

res = collect_permutation_results(".")
write_permut2files(res)
