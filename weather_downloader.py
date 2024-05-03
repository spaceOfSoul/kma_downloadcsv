from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
import os

ID = ''
PW = ''
URL = ''
PATH =''

class wait_for_display_to_be_none(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        display = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", element)
        return display == "none"

def login(driver):
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
    tg_id.send_keys(ID) # Here
    time.sleep(1)

    tg_pw.click()
    tg_pw.send_keys(PW) # And here
    time.sleep(1)

    enter_btn = driver.find_element(By.XPATH, '//*[@id="loginbtn"]')
    enter_btn.click()
    time.sleep(1)

def readyToDownload(driver):
    driver.get(URL) # asos
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

def download(driver,m,d):
    date = '2023'+ str(m).zfill(2) + str(d).zfill(2)
        
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

    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "divPopupTemp"))
        )
        raise Exception("Error: #divPopupTemp element is present on the page.")
    except :
        print("No #divPopupTemp element found. Continuing with the process.")

    time.sleep(1)

def reset_session_and_cookies(driver):
    driver.delete_all_cookies()
    driver.refresh()


def download_month(m):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": PATH, 
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        "profile.default_content_setting_values.automatic_downloads": 1
    })
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.set_window_size(1920, 1080) 
    checked = False

    login(driver)
    time.sleep(1)
    readyToDownload(driver)

    months_2023 = [None,(1,31),(2,28),(3,31),(4,30),(5,31),(6,30),(7,31),(8,31),(9,30),(10,31),(11,30),(12,31)]

    download_month = [m]

    time.sleep(1)

    for i in download_month:
        for j in range(1,months_2023[i][1]+1):
            files = os.listdir(PATH)
            file_count = len(files)
            re = True
            while re:
                print(f"{i}월 {j}일")
                current_url = driver.current_url

                if current_url != URL:
                    while True:
                        try:
                            reset_session_and_cookies(driver)
                            login(driver)
                            time.sleep(1)
                            readyToDownload(driver)
                            print('re login')
                            break
                        except:
                            time.sleep(1)
                            continue
                        
                try:
                    download(driver,i,j)
                    time.sleep(1)
                    #//*[@id="loading-mask"]
                    while True:
                        try:
                            WebDriverWait(driver, 120).until(wait_for_display_to_be_none((By.XPATH, '//*[@id="loading-mask"]')))
                            break
                        except:
                            continue
                except:
                    while True:
                        try:
                            reset_session_and_cookies(driver)
                            login(driver)
                            time.sleep(1)
                            readyToDownload(driver)
                            print('re login')
                        except:
                            time.sleep(1)
                            continue
                        time.sleep(1)
                        try:
                            download(driver,i,j)
                            time.sleep(1)
                            while True:
                                try:
                                    WebDriverWait(driver, 120).until(wait_for_display_to_be_none((By.XPATH, '//*[@id="loading-mask"]')))
                                    break
                                except:
                                    continue
                        except:
                            time.sleep(1)
                            continue
                time.sleep(1)

                if not checked:
                    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="reqstPurposeCd7"]')))
                    btn = driver.find_element(By.XPATH, '//*[@id="reqstPurposeCd7"]')
                    btn.click()
                    time.sleep(0.5)
                    btn = driver.find_element(By.XPATH, '//*[@id="wrap-datapop"]/div/div[2]/div/a[2]')
                    btn.click()
                    time.sleep(0.5)
                    checked = True
                WebDriverWait(driver, 120).until(wait_for_display_to_be_none((By.XPATH, '//*[@id="loading-mask"]')))

                files = os.listdir(PATH)
                current_file_count = len(files)
                print("old : ", file_count)
                print("current : ",current_file_count)
                if current_file_count > file_count:
                    re = False

    print(f'{m}`s clear')
    time.sleep(2)