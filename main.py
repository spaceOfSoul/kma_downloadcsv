import weather_downloader
import sys
import os
from dotenv import load_dotenv

load_dotenv()

####################################
# 여기에 본인 아이디와 비번을 적어주세요.
####################################
weather_downloader.ID = os.getenv('ID')
weather_downloader.PW = os.getenv('PW')
weather_downloader.URL = os.getenv('URL')
weather_downloader.PATH = os.getenv('PATH')

####################################
# 여기에 다운로드 할 월을 넣어주세요.
# ex) 다운로드 할 날짜 : 1월, 2월, 3월
# months = [1,2,3]
####################################
months = [int(month) for month in sys.argv[1:]]

for i in months:
    weather_downloader.download_month(i)
print('all clear!')