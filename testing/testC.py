#pythcopy pasta from http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python
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


import string
import random

def random_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def randomgmail():
    return random_generator() + "@gmail.com"


def random_name():
    return ''.join(random.choice(string.ascii_lowercase) for x in range(random.randint(5,10)))

my_path = "http://127.0.0.1:5000/"
passw = "password"
first = ""
last = ""
gmail = randomgmail()

userg1 = ""
userg2 = ""


def my_path():
#    temp = os.getcwd()
 #   my_path = "file://" + temp[:-12] + "cinder/public/"    
    return my_path

def init_driver():
    driver = webdriver.firefox()
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


        #login into an account and navigate matches page

    def test_runtest1(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        elem = driver.find_element_by_xpath("//input[@name='email']")
        elem.send_keys("teammates@gmail.com")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//input[@name='email']/following::input[1]")
        elem.send_keys("pineapple")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//button[@id='log']").click()
        time.sleep(1)
        elem = driver.find_element_by_xpath("//a[@href='/profile']").click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/5);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight/5,document.body.scrollHeight/2);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight/2,document.body.scrollHeight);")                        
        time.sleep(1)
        """
        elem = driver.find_element_by_xpath("//a[@href='/matches']").click()
        time.sleep(2)
        elem = driver.find_element_by_xpath("//a[@class='btn btn-primary']/following::a[1]").click()
        time.sleep(1)
        elem = driver.find_element_by_xpath("//button[@id='date_button']").click()
        time.sleep(1)
        elem = driver.find_element_by_xpath("//input[@id='time']")
        elem.send_keys("11:00")
        time.sleep(2)
        """
        
        #login into an account and navigate feedbackpage
    def test_runtest2(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        elem = driver.find_element_by_xpath("//input[@name='email']")
        elem.send_keys("teammates@gmail.com")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//input[@name='email']/following::input[1]")
        elem.send_keys("pineapple")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//button[@id='log']").click()
        time.sleep(1)
        elem = driver.find_element_by_xpath("//a[@href='/profile']").click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/5);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight/5,document.body.scrollHeight/2);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight/2,document.body.scrollHeight);")                        
        time.sleep(1)
        elem = driver.find_element_by_xpath("//a[@href='/your_feedback']").click()
        time.sleep(2)
        elem = driver.find_element_by_xpath("//a[@href='/give_feedback']").click()
        time.sleep(1)
        """
        elem = driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        time.sleep(3)
        elem = driver.find_element_by_xpath("//textarea[@id='feedBackTextArea']")
        elem.send_keys("his head is too big, he isn't as smart as he thinks")
        time.sleep(3)
        elem = driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(3)    
        """
        
        #create a new user acount
    def test_runtest3(self):
        first = random_name()
        last = random_name()

        f = open("../usernames.txt","a+")
        f.write(gmail)
        f.write("\n")
        f.close()
        
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_name("sign").click()
        driver.implicitly_wait(30)
        time.sleep(5)
        elem = driver.find_element_by_name("first")
        elem.send_keys(first)
        time.sleep(1)
        elem = driver.find_element_by_name("last")
        elem.send_keys(last)
        time.sleep(1)
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[4]")
        elem.send_keys(gmail)
        time.sleep(1)
        elem = driver.find_element_by_name("pswd")
        elem.send_keys(passw)
        time.sleep(1)
        elem = driver.find_element_by_name("age")
        elem.send_keys(random.randint(18,70))
        time.sleep(1)
        elem = driver.find_element_by_name("location")
        elem.send_keys("Toronto")
        elem.send_keys(Keys.ENTER)
        time.sleep(1)
        elem = driver.find_element_by_name("gender")
        if random.randint(0,100) % 2 == 0:
            elem.send_keys(Keys.DOWN)
        time.sleep(1)
        elem.send_keys(Keys.ENTER)
        time.sleep(1)
        elem = driver.find_element_by_name("interest")
        if random.randint(0,100) % 2 == 0:
            elem.send_keys(Keys.DOWN)
        time.sleep(1)
        elem.send_keys(Keys.ENTER)
        time.sleep(1)
        elem = driver.find_element_by_name("bio")
        elem.send_keys(random_generator(30))
        time.sleep(1)
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[" + str(random.randint(10,11)) + "]").click()
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[" + str(random.randint(12,13)) + "]").click()
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[" + str(random.randint(14,15)) + "]").click()
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[" + str(random.randint(16,17)) + "]").click()
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[" + str(random.randint(18,19)) + "]").click()
        elem = driver.find_element_by_name("profile_image").send_keys(os.getcwd()[:-5] + "/defaultpic.png")
        time.sleep(3)
        elem = driver.find_element_by_id("modal-submit").click()
        time.sleep(1)

        #sign in into the new account just newly made and swipe
    def test_runtest4(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        elem = driver.find_element_by_xpath("//input[@name='email']")
        elem.send_keys(gmail)
        time.sleep(1)
        elem = driver.find_element_by_xpath("//input[@name='email']/following::input[1]")
        elem.send_keys(passw)
        time.sleep(1)
        elem = driver.find_element_by_xpath("//button[@id='log']").click()
        time.sleep(1)
        elem = driver.find_element_by_xpath("//a[@href='/profile']").click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/5);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight/5,document.body.scrollHeight/2);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight/2,document.body.scrollHeight);")                        
        time.sleep(1)
        elem = driver.find_element_by_xpath("//a[@href='/meet']").click()
        driver.implicitly_wait(30)
        time.sleep(2)
        elem = driver.find_element_by_xpath("//span[@id='chevron-right']").click()
        time.sleep(3)
        elem = driver.find_element_by_xpath("//span[@id='chevron-right']").click()
        time.sleep(3)
        elem = driver.find_element_by_xpath("//span[@id='chevron-left']").click()
        time.sleep(3)
        elem = driver.find_element_by_xpath("//button[@class='nav-btn']").click()
        time.sleep(3)


    def test_runtest5(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        elem = driver.find_element_by_xpath("//input[@name='email']")
        elem.send_keys("nancydrew@gmail.com")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//input[@name='email']/following::input[1]")
        elem.send_keys("password")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//button[@id='log']").click()
        time.sleep(1)
        elem = driver.find_element_by_xpath("//a[@href='/your_feedback']").click()
        time.sleep(2)
        elem = driver.find_element_by_xpath("//a[@href='/give_feedback']").click()
        time.sleep(1)
        elem = driver.find_element_by_xpath("//textarea[@name='feedBackTextArea']")
        elem.send_keys("so are you like, the real Tina Fey, cause I am a detective")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//button[@class='btn btn-primary']")
        time.sleep(3)
        #remember to add back click
        
        #fill in user for john and upload john.jpeg
    def test_runtest6(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        driver.find_element_by_name("sign").click()
        driver.implicitly_wait(30)
        time.sleep(5)
        elem = driver.find_element_by_name("first")
        elem.send_keys("John")
        time.sleep(1)
        elem = driver.find_element_by_name("last")
        elem.send_keys("Winchester")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[4]")
        elem.send_keys("coolio@gmail.com")
        time.sleep(1)
        elem = driver.find_element_by_name("pswd")
        elem.send_keys(passw)
        time.sleep(1)
        elem = driver.find_element_by_name("age")
        elem.send_keys('25')
        time.sleep(1)
        elem = driver.find_element_by_name("location")
        elem.send_keys("Toronto")
        elem.send_keys(Keys.ENTER)
        time.sleep(1)
        elem = driver.find_element_by_name("interest")
        elem.send_keys(Keys.DOWN)
        time.sleep(1)
        elem.send_keys(Keys.ENTER)
        time.sleep(1)
        elem = driver.find_element_by_name("bio")
        elem.send_keys('I like cars.')
        time.sleep(1)
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[11]").click()
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[12]").click()
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[14]").click()
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[17]").click()
        elem = driver.find_element_by_xpath("//input[@name='email']//following::input[19]").click()
        elem = driver.find_element_by_name("profile_image").send_keys(os.getcwd()[:-5] + "/john.jpeg")
        time.sleep(3)
        elem = driver.find_element_by_id("modal-submit")
        time.sleep(1)
        
    

    """       
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
`        elem = driver.find_element_by_name("sign").click()
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
 """       
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
    print "http://127.0.0.1:5000/"
    print  os.getcwd()[:-5]


    unittest.main()
