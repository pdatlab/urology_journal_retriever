

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import shutil


profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList",2);
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference("browser.download.dir","c:\\BJUI\landing");
profile.set_preference("browser.popups.showPopupBlocker", False);
profile.set_preference("browser.helperApps.alwaysAsk.force", False);
profile.update_preferences()
# This sets browser preferences, such as download directory and allowing popups and direct downloads.

driver = webdriver.Firefox(firefox_profile=profile, executable_path=r"C:\Program Files\Mozilla Firefox\Driver\geckodriver.exe")
# driver loaded with specified profile and webdriver path

start_year = int()
volume_issue = []

def _years(start_year,end_year):
    while start_year <= end_year:
        driver.get("https://bjui-journals.onlinelibrary.wiley.com/loi/1464410x/year/"+str(start_year))
        driver.implicitly_wait(40)
        _issues()
        start_year += 1
        
def _issues():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                    ((By.CLASS_NAME, "visitable")))   
    issue_list = driver.find_elements_by_class_name('visitable')
    issue_link = driver.current_url
    
    issue_num = 0
    while issue_num <= len(issue_list):
        issue_list = driver.find_elements_by_class_name('visitable')
        issue_list[issue_num].click()
        volume_issue = driver.find_element_by_class_name('cover-image__parent-item').text
        volume_issue.split(',')
        volume_issue.replace(' ','_')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CLASS_NAME, "issue-item__title"))) 
        article_list = driver.find_elements_by_class_name('issue-item__title')
        article_link = driver.current_url
        issue_num += 1
        
        article_num = 0
        while article_num <= len(article_list):
            article_list = driver.find_elements_by_class_name('issue-item__title')
            article_list[article_num].click()
            # _infoGrabber()
            driver.get(article_link)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CLASS_NAME, "issue-item__title")))
            article_num += 1
        driver.get(issue_link)

        
def _infoGrabber():
    title = driver.find_element_by_class_name('citation__title').text
    page = driver.find_element_by_class_name('page-range').text
    driver.find_element_by_class_name('coolBar__ctrl pdf-download').click()
    driver.send_keys("g")
    # shortcut for opening a download popup in the BJUI journal viewer
    
    filename = _fileName(10)
    source = "c:\\BJUI\landing" f"\{filename}" ".pdf" 
    destination =  "c:\\BJUI\landing" f"\{volume_issue[0]}" f"_{start_year}" f"\{volume_issue[1]}"
    f"\{title}" ".pdf" 
    path = os.path.join("c:\\", destination)
    if not os.path.exists(path):
        os.mkdir(path)
    # looks for existing file path, creates if absent    
    shutil.move(source,destination)
  
def _fileName(waitTime):
    # driver.execute_script("window.open()")
    # WebDriverWait(driver,10).until(EC.new_window_is_opened)
    # driver.switch_to.window(driver.window_handles[-1])
    driver.get("about:downloads")
    endTime = time.time()+waitTime
    while True:
        try:
            fileName = driver.execute_script("return document.querySelector('#contentAreaDownloadsView .downloadMainArea .downloadContainer description:nth-of-type(1)').value")
            if fileName:
                return fileName
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break
        # this goes into downloads and finds the name of the most recently downloaded file
_years(1996, 1997)


