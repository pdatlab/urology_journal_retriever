

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


import time
import os
import shutil

# Setup of chrome preferences (download directory) -------
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "C:\journals\BJUI\Landing"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)

volume_issue = []


def years(start_year,end_year):
    while start_year <= end_year:
        driver.get("https://bjui-journals.onlinelibrary.wiley.com/loi/1464410x/year/"+str(start_year))
        driver.implicitly_wait(40)
        _issues(start_year)
        start_year += 1
        
def _issues(start_year):
    global volume_issue
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                    ((By.CLASS_NAME, "visitable")))   
    issue_list = driver.find_elements_by_class_name('visitable')
    issue_link = driver.current_url
    
    issue_num = 0
    while issue_num <= len(issue_list):
        issue_list = driver.find_elements_by_class_name('visitable')
        issue_list[issue_num].click()
        time.sleep(3)
        volume_issue = driver.find_element_by_class_name('cover-image__parent-item').text
        volume_issue = volume_issue.replace('Volume ','V')
        volume_issue = volume_issue.replace('Issue ','I')
        volume_issue = volume_issue.split(", ")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CLASS_NAME, "issue-item__title"))) 
        article_list = driver.find_elements_by_class_name('issue-item__title')
        article_link = driver.current_url
        issue_num += 1
        
        article_num = 0
        while article_num <= len(article_list):
            article_list = driver.find_elements_by_class_name('issue-item__title')
            article_list[article_num].click()
            time.sleep(3)
            _infoGrabber(start_year)
            driver.get(article_link)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CLASS_NAME, "issue-item__title")))
            article_num += 1
        driver.get(issue_link)

        
def _infoGrabber(start_year):
    title = driver.find_element_by_class_name('citation__title').text
    page = driver.find_element_by_class_name('page-range').text
    doi = driver.find_element_by_class_name('epub-doi').text
    doi = doi.replace('https://doi.org/','')
    doi = doi.replace('.','_')
    doi = doi.replace('/','_')
    pdflink = driver.find_element_by_class_name('coolBar__ctrl.pdf-download').get_attribute('href')
    driver.get(pdflink)
    time.sleep(3)
    rename = f"{volume_issue[0]}"f"_{volume_issue[1]}"f"_{doi}" f"_{title}.pdf"
    if len(rename) >= 255:
        rename = rename[0:255]
    if not driver.find_elements_by_id('app-navbar'):
        print('Article not available for download: 'f"{rename}")
        return
    driver.find_element_by_tag_name('body').send_keys('g')
    time.sleep(2)
    # shortcut for opening a download popup in the BJUI journal viewer
    filename = _fileName(10)
    source = "c:\\BJUI\\landing" f"\\{filename}"
   
    destination =  "c:\\BJUI" f"\\{start_year}"
    path = os.path.join(destination)
    if not os.path.exists(path):
        os.makedirs(path)
    # looks for existing file path, creates if absent    
    shutil.move(source,destination)
    try:
        os.rename(f"{destination}"f"\\{filename}",f"{destination}"f"\\{rename}")
    except FileExistsError:
        os.remove(f"{destination}"f"\\{filename}")

def _fileName(waitTime):
    # driver.execute_script("window.open()")
    # WebDriverWait(driver,10).until(EC.new_window_is_opened)
    # driver.switch_to.window(driver.window_handles[-1])
    driver.get("chrome://downloads/")
    endTime = time.time()+waitTime
    while True:
        try:
            # https://stackoverflow.com/questions/34548041/selenium-give-file-name-when-downloading
            # downloadPercentage = driver.execute_script(
            #     "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            time.sleep(10)
            # if downloadPercentage == 100:
                # return the file name once the download is completed
            return driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break
            # this goes into downloads and finds the name of the most recently downloaded file

years(1996, 1997)



