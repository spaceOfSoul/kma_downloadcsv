import weather_downloader

####################################
# 여기에 본인 아이디와 비번을 적어주세요.
####################################
weather_downloader.ID = ''
weather_downloader.PW = ''

####################################
# 여기에 다운로드 할 월을 넣어주세요.
# ex) 다운로드 할 날짜 : 1월, 2월, 3월
# months = [1,2,3]
####################################
months = [2]

for i in months:
    weather_downloader.download_month(i)
print('all clear!')