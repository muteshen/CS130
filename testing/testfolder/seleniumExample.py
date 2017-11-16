#copy pasta from http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python
#you need to "pip install selenium" and the Firefox webdriver(geckodriver)
#see https://github.com/mozilla/geckodriver/releases
#add geckodriver to your path/ put the exe in you usr/local/bin then this should work
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

my_path = "file:///home/avwong13/Desktop/cs130-cinder/testing/venv/testfolder/"

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookup(driver, query):
    driver.get("http://www.google.com")
    try:
        box = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "q")))
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "btnK")))
        box.send_keys(query)
        button.click()
    except TimeoutException:
        print("Box or Button not found in google.com")

def test1(driver,path):
    driver.get(my_path + "home.html")
    driver.find_element_by_link_text('Meet People').click()
    time.sleep(3)

class testing(unittest.TestCase):    
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_runtest1(self):
        driver = self.driver
        driver.get(my_path + "home.html")
        driver.find_element_by_link_text('Meet People').click()
        time.sleep(1)

    def test_runtest2(self):
        driver = self.driver
        driver.get(my_path + "home.html")
        driver.find_element_by_link_text('Feedback').click()
        driver.find_element_by_link_text('Meet People').click()
        driver.find_element_by_link_text('Cinder').click()
        time.sleep(1)
        
    def tearDown(self):
        self.driver.close()

"""
class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()
"""

if __name__ == "__main__":
#    driver = init_driver()
    

   # lookup(driver, "Selenium")
 #   test1(driver, my_path)
  #  time.sleep(5)
   # driver.quit()
    unittest.main()
