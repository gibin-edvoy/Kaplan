from selenium import webdriver
import geckodriver_autoinstaller
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Firefox selenium settings.
# geckodriver_autoinstaller.install()
# profile = webdriver.FirefoxProfile('/home/gibi/.mozilla/firefox/rvbevz2f.default')
# profile.set_preference("dom.webdriver.enabled", False)
# profile.set_preference('useAutomationExtension', False)
# profile.update_preferences()
# desired = DesiredCapabilities.FIREFOX
# driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired)

driver = webdriver.Chrome("/home/gibi/PycharmProjects/kaplan/chromedriver")

url = "https://www.kaplanpathways.com/degree-finder/#/search-result?status=1&prefer-study=1&institution_short_name" \
      "=Arizona-State-University-Downtown-Phoenix-Campus&institution_short_name=Arizona-State-University-Lake-Havasu" \
      "-Campus&subject_area_name=&university=38,39 "

driver.maximize_window()
# Open url in browser
driver.get(url)
# Wait time in sec(s)
time.sleep(5)
try:

    # click on accept
    driver.find_element_by_id("ccc-notify-accept").click()
    time.sleep(2)
except:
    print("Already accepted or button not available...!")

try:
    for i in range(1, 10):
        #   scroll to page bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Click on show more button
        driver.find_element_by_xpath("/html/body/div[5]/main/div/div/app-root/app-search-result/div/div[2]/div[2]/div[2]/button[1]").click()
except:
    pass

# Get complete course list
course_list = driver.find_elements_by_xpath("//*[@class='wrap-result']")

for course in course_list:
    try:
        time.sleep(5)

        course.click()
        c_name = course.find_element_by_xpath('./div/div/p[2]').text
        print(c_name)
    except:
        print("⛑ Element is not clickable ")
