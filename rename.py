import os
import re

import os
import re

directory_path = "./weaderdata_asos/"

file_list = os.listdir(directory_path)

def get_number_from_filename(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None

sorted_file_list = sorted(file_list, key=get_number_from_filename)

date_counter = 20220401

for i in sorted_file_list:
    new_filename = f"asos_gwd_{date_counter}.csv"
    os.rename(os.path.join(directory_path, i), os.path.join(directory_path, new_filename))
    date_counter += 1
