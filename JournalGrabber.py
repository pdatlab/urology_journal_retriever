

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import os
import shutil

driver = webdriver.Firefox(executable_path=r"C:\Program Files\Mozilla Firefox\Driver\geckodriver.exe")

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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CLASS_NAME, "issue-item__title"))) 
        article_list = driver.find_elements_by_class_name('issue-item__title')
        article_link = driver.current_url
        issue_num += 1
        
        article_num = 0
        while article_num <= len(article_list):
            article_list = driver.find_elements_by_class_name('issue-item__title')
            article_list[article_num].click()
            # _infograbber()
            driver.get(article_link)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CLASS_NAME, "issue-item__title")))
            article_num += 1
        driver.get(issue_link)

        
def _infograbber():
    title = driver.find_element_by_class_name('citation__title').text
    page = driver.find_element_by_class_name('page-range').text
    driver.find_element_by_class_name('coolBar__ctrl pdf-download').click()
    driver.send_keys("g")
    # shortcut for opening a download popup in the BJUI journal viewer
    # TODO Rename file to title+page?
    # shutil.move(download path,requested path)
_years(1996, 1997)

"""
EXAMPLE of firefox autodownload solution from stackx 
(link:https://sqa.stackexchange.com/questions/2197/how-to-download-a-file-using-seleniums-webdriver)

I do not think download directory can be changed while in a loop. Files may have to be sorted by assigned name
    Assigning name to file by renaming last downloaded (Link:
                                            https://stackoverflow.com/questions/34548041/selenium-give-file-name-when-downloading)

FirefoxProfile fxProfile = new FirefoxProfile();

fxProfile.setPreference("browser.download.folderList",2);
fxProfile.setPreference("browser.download.manager.showWhenStarting",false);
fxProfile.setPreference("browser.download.dir","c:\\mydownloads");
profile.setPreference(“browser.popups.showPopupBlocker”, false);
setPreference("browser.helperApps.alwaysAsk.force", false);

WebDriver driver = new FirefoxDriver(fxProfile);
driver.navigate().to("http://www.foo.com/bah.csv");
"""
