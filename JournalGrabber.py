

from selenium import webdriver
# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver = webdriver.Chrome(ChromeDriverManager().install())

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



_years(1996, 1997)
        # TODO Downloader goes here
        
# def _infograbber(self):
#     title = driver.find_element_by_class_name('citation__title')
#     volume = driver.find_element_by_class_name('volume-issue')
#     page = driver.find_element_by_class_name('page-range')
    # TODO copy info
    # driver.find_element_by_class_name('coolBar__ctrl pdf-download').click()


"""
EXAMPLE of firefox autodownload solution from stackx 
(link:https://sqa.stackexchange.com/questions/2197/how-to-download-a-file-using-seleniums-webdriver)

FirefoxProfile fxProfile = new FirefoxProfile();

fxProfile.setPreference("browser.download.folderList",2);
fxProfile.setPreference("browser.download.manager.showWhenStarting",false);
fxProfile.setPreference("browser.download.dir","c:\\mydownloads");
fxProfile.setPreference("browser.helperApps.neverAsk.saveToDisk","text/csv");

WebDriver driver = new FirefoxDriver(fxProfile);
driver.navigate().to("http://www.foo.com/bah.csv");
"""