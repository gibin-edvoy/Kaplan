from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
# driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

driver = webdriver.Chrome("/home/gibi/PycharmProjects/kaplan/chromedriver", chrome_options=options)

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
        driver.find_element_by_xpath("/html/body/div[5]/main/div/div/app-root/app-search-result/div/div[2]/div["
                                     "2]/div[2]/button[1]").click()
except:
    pass

# Get complete course list
course_list = driver.find_elements_by_xpath("//*[@class='wrap-result'][1]")

# loop through each course
for course in course_list:
    try:
        time.sleep(2)
        # Scroll to each element to get the trigger
        actions = ActionChains(driver)
        actions.move_to_element(course).perform()
        # click in the course to expand
        course.click()
        c_name = course.find_element_by_xpath('./div/div/p[2]').text
        u_name = course.find_element_by_xpath('./div/div/p[2]').text
        college = driver.find_element_by_xpath('//*[@class="degree-info"]/p/span').text

        print(c_name)

        # Click on the course again to close it.
        course.click()
    except:
        print("⛑ Element is not clickable ")
