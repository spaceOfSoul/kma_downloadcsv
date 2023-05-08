from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip
from dotenv import load_dotenv
import os

load_dotenv()

driver = webdriver.Chrome()
cheched = False
####################################
#여기에 본인 아이디와 비번을 적어주세요.
####################################
ID = ''
PW = ''

class wait_for_display_to_be_none(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        display = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", element)
        return display == "none"

def login():
    driver.get('https://data.kma.go.kr/cmmn/main.do')

    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginBtn"]')))
    WebDriverWait(driver, 120).until(wait_for_display_to_be_none((By.XPATH, '//*[@id="loading-mask"]')))
    login_btn = driver.find_element(By.XPATH, '//*[@id="loginBtn"]')
    login_btn.click()
    time.sleep(1)

    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginId"]')))
    WebDriverWait(driver, 120).until(wait_for_display_to_be_none((By.XPATH, '//*[@id="loading-mask"]')))
    tg_id = driver.find_element(By.XPATH, '//*[@id="loginId"]')
    tg_pw = driver.find_element(By.XPATH, '//*[@id="passwordNo"]')

    tg_id.click()
    pyperclip.copy(ID)
    tg_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    tg_pw.click()
    pyperclip.copy(PW)
    tg_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    enter_btn = driver.find_element(By.XPATH, '//*[@id="loginbtn"]')
    enter_btn.click()
    time.sleep(0.5)

def readyToDownload():
    driver.get('https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36')
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dataFormCd"]')))
    WebDriverWait(driver, 120).until(wait_for_display_to_be_none((By.XPATH, '//*[@id="loading-mask"]')))
    list1 = driver.find_element(By.XPATH, '//*[@id="dataFormCd"]')
    list1.click()
    time.sleep(0.5)

    minbtn = driver.find_element(By.XPATH, '//*[@id="dataFormCd"]/option[5]')
    minbtn.click()
    time.sleep(0.5)

    btn = driver.find_element(By.XPATH, '//*[@id="ztree_2_check"]')
    btn.click()
    time.sleep(0.5)

    btn = driver.find_element(By.XPATH, '//*[@id="ztree1_1_check"]')
    btn.click()
    time.sleep(0.5)

def download(m,d):
    date = '2022'+ str(m).zfill(2) + str(d).zfill(2)
        
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="startDt_d"]')))
    WebDriverWait(driver, 120).until(wait_for_display_to_be_none((By.XPATH, '//*[@id="loading-mask"]')))
    
    input_field = driver.find_element(By.XPATH, '//*[@id="startDt_d"]')
    input_field.clear()
    input_field.send_keys(date)
    time.sleep(0.5)

    input_field = driver.find_element(By.XPATH, '//*[@id="endDt_d"]')
    input_field.clear()
    input_field.send_keys(date)
    time.sleep(0.5)
    
    btn = driver.find_element(By.XPATH, '//*[@id="wrap_content"]/div[4]/div[1]/div/a[1]')
    btn.click()

login()
readyToDownload()

months_2022 = [None,(1,31),(2,28),(3,31),(4,30),(5,31),(6,30),(7,31),(8,31),(9,30),(10,31),(11,30),(12,31)]

####################################
#여기에 다운로드 할 월을 넣어주세요.
#ex) 다운로드 할 날짜 : 1월, 2월, 3월
#download_month = [1,2,3]
####################################
download_month = [4,5,6]

for i in download_month:
    for j in range(1,months_2022[i][1]+1):
        current_url = driver.current_url

        if current_url != 'https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36':
            while True:
                try:
                    login()
                    readyToDownload()
                    break
                except:
                    continue
    
        try:
            download(i,j)
        except:
            while True:
                try:
                    login()
                    readyToDownload()
                    break
                except:
                    continue
            download(i,j)
        time.sleep(1)
        
        #//*[@id="loading-mask"]
        
        WebDriverWait(driver, 120).until(wait_for_display_to_be_none((By.XPATH, '//*[@id="loading-mask"]')))

        if not cheched:
            WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="reqstPurposeCd7"]')))
            btn = driver.find_element(By.XPATH, '//*[@id="reqstPurposeCd7"]')
            btn.click()
            time.sleep(0.5)
            btn = driver.find_element(By.XPATH, '//*[@id="wrap-datapop"]/div/div[2]/div/a[2]')
            btn.click()
            time.sleep(0.5)
            cheched = True
        WebDriverWait(driver, 120).until(wait_for_display_to_be_none((By.XPATH, '//*[@id="loading-mask"]')))

print('all clear')