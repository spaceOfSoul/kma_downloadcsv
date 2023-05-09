import os
import re
from itertools import chain

directory_path = "./change_name/"

file_list = os.listdir(directory_path)

def get_number_from_filename(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None

sorted_file_list = sorted(file_list, key=get_number_from_filename)

months_2022 = [None,(1,31),(2,28),(3,31),(4,30),(5,31),(6,30),(7,31),(8,31),(9,30),(10,31),(11,30),(12,31)]
downloaded_months = [4,5,6]

# 월별 일자 생성
dates = list(chain.from_iterable([[(month, day) for day in range(1, months_2022[month][1] + 1)] for month in downloaded_months]))

# 파일 이름 변경
for filename, date in zip(sorted_file_list, dates):
    month, day = date
    new_filename = f"asos_gwd_2022{month:02d}{day:02d}.csv"
    os.rename(os.path.join(directory_path, filename), os.path.join(directory_path, new_filename))