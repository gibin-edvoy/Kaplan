from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.
# driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

driver = webdriver.Chrome("/home/gibi/PycharmProjects/kaplan/chromedriver")

# url = "https://www.kaplanpathways.com/degree-finder/#/search-result?status=1&prefer-study=1&institution_short_name=Arizona-State-University-Downtown-Phoenix-Campus&institution_short_name=Arizona-State-University-Lake-Havasu-Campus&subject_area_name=&university=38,39"
url = "https://www.kaplanpathways.com/degree-finder/#/search-result?status=1&institution_short_name=Arizona-State-University-Lake-Havasu-Campus&subject_area_name=&prefer-study=1&university=39"

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
course_list = driver.find_elements_by_xpath("//*[@class='wrap-result']")
print("Total courses: ", len(course_list))

to_excel = {}

college = ""
degree = ""
intakes = ""
fee = ""
# loop through each course
i = 1
k = 0
for course in course_list:
    try:
        print("Current check: ", i)
        i += 1
        time.sleep(2)
        # Scroll to each element to get the trigger
        actions = ActionChains(driver)
        actions.move_to_element(course).perform()
        # click in the course to expand
        course.click()
        time.sleep(1)

        c_name = course.find_element_by_xpath('./div/div/p[2]').text
        u_name = course.find_element_by_xpath('./div/div[3]/p').text
        source_url = driver.find_element_by_xpath("//*[@class='link-more']").get_attribute("href")

        d_info = driver.find_elements_by_xpath('//*[@class="degree-info"]/p')
        for info in d_info:
            if "Academic" in info.text:
                college = info.find_element_by_tag_name("span").text
            if "duration" in info.text:
                degree = info.find_element_by_tag_name("span").text
            if "intake" in info.text:
                intakes = info.find_element_by_tag_name("span").text
            if "fee" in info.text:
                fee = info.find_element_by_tag_name("span").text

        list_intakes = intakes.split(",")
        # j = 0

        for split_intake in list_intakes:
            k += 1
            print(i+k)
            curr_iter = {}

            curr_iter["ID"] = k
            curr_iter["Course name"] = c_name
            curr_iter["uni"] = u_name
            curr_iter["Source_url"] = source_url
            curr_iter["campus"] = college
            curr_iter["duration"] = degree
            curr_iter['intake'] = split_intake
            curr_iter['fees'] = fee

            print(curr_iter)

            to_excel[i + k] = curr_iter
            # j += 1

        # print("c_name: ", c_name)
        # print("u_name: ", u_name)
        # print("college: ", college)
        # print("degree: ", degree)
        # print("intakes: ", intakes)
        # print("fee: ", fee)
        # print("source_url: ", source_url)

        print("_" * 30)

        # Click on the course again to close it.
        course.click()
    except Exception as e:
        print(e)

df = pd.DataFrame(to_excel)
df1 = df.transpose()
print(df1)

writer = pd.ExcelWriter("dataframe.xlsx", engine='xlsxwriter')
df1.to_excel(writer, sheet_name="Kaplan", index=False)
writer.save()

driver.close()