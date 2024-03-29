#copy pasta from http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python
#you need to "pip install selenium" and the Firefox webdriver(geckodriver)
#see https://github.com/mozilla/geckodriver/releases
#add geckodriver to your path/ put the exe in you usr/local/bin then this should work
import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

my_path = "file:///home/avwong13/Desktop/cs130-cinder/cinder/public/"
def my_path():
    temp = os.getcwd()
    my_path = "file://" + temp[:-12] + "cinder/public/"    
    return my_path

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
        driver.get(my_path() + "home.html")
        driver.find_element_by_link_text('Meet People').click()
        time.sleep(1)

    def test_runtest3(self):
        driver = self.driver
        driver.get(my_path() + "home.html")
        driver.find_element_by_link_text('Feedback').click()
        time.sleep(2)
        driver.find_element_by_id('giveFeedBackBtn').click()
        time.sleep(3)
        elem = driver.find_element_by_id('feedBackTextArea')
        elem.send_keys("had a great time, but next time take a shower before coming.")
        time.sleep(4)


    def test_runtest2(self):
        driver = self.driver
        driver.get(my_path() + "home.html")
        elem = driver.find_element_by_name("first")
        elem.send_keys("John")
        time.sleep(1)
        elem = driver.find_element_by_name("last")
        elem.send_keys("Winchest")
        time.sleep(1)
        elem.send_keys(Keys.ENTER)
        time.sleep(1)
        elem = driver.find_element_by_name("email")
        elem.send_keys("coolio@gmail.com")
        time.sleep(1)
        elem = driver.find_element_by_name("password")
        elem.send_keys("calypso")
        elem = driver.find_element_by_name("sign").click()
        time.sleep(1)
        elem = driver.find_element_by_name("age")
        elem.send_keys('25')
        time.sleep(1)
        elem = driver.find_element_by_name("interest")
        elem.send_keys(Keys.DOWN)
        time.sleep(3)
        elem.send_keys(Keys.ENTER)
        time.sleep(3)
        elem = driver.find_element_by_name("bio")
        elem.send_keys('I like cars.')
        time.sleep(1)
        elem = driver.find_element_by_name("sub")
        driver.find_element_by_name("sub")

    def test_runtest4(self):
        driver = self.driver
        driver.get(my_path() + "meet.html")
        driver.find_element_by_id('chevron-right').click()
        time.sleep(4)
        
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
    print my_path()

    unittest.main()
