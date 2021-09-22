

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(ChromeDriverManager().install())

# todo break down layers of navigation into classes EX:
    
def _years(start_year,end_year):
    while start_year <= end_year:
        driver.get("https://bjui-journals.onlinelibrary.wiley.com/loi/1464410x/year/"+str(start_year))
        driver.implicitly_wait(40)
        _issues()
        start_year = start_year + 1
        
def _issues():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                    ((By.CLASS_NAME, "visitable")))   
    issuelist = driver.find_elements_by_class_name('visitable')
    for x in issuelist:
        x.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CLASS_NAME, "issue-item__title"))) 
        articlelist = driver.find_elements_by_class_name('issue-item__title')
        
        for x in articlelist:
            articlelist = driver.find_elements_by_class_name('issue-item__title')
            x.click()
            # _infograbber()
            driver.back()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                        ((By.CLASS_NAME, "issue-item__title")))
        driver.back()



_years(1996, 1997)
        # TODO Downloader goes here, also figure out how to return to previous page (save url & driver.get?)
        
# def _infograbber(self):
#     title = driver.find_element_by_class_name('citation__title')
#     volume = driver.find_element_by_class_name('volume-issue')
#     page = driver.find_element_by_class_name('page-range')
    # TODO copy info
    # driver.find_element_by_class_name('coolBar__ctrl pdf-download').click()
