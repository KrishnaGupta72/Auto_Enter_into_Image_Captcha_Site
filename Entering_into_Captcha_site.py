# Amazon product price tracker using Python

# importing libraries
from requests import get
import requests
from bs4 import BeautifulSoup
import schedule

import os
import time
from selenium import webdriver

captcha_text=''

def captch_Img_Text(resp):
    html_soup = BeautifulSoup(resp, "lxml")
    #Get captcha image url value
    imageurl_container = html_soup.find("div", {"class": "a-row a-text-center"}).findChildren()
    for res in imageurl_container:
        captcha_img_url = res['src']

    #Hit captcha image url and download captcha image file.
    with open("Captcha_image.jpg", 'wb') as f:
        response = requests.get(captcha_img_url)
        f.write(response.content)

    driver = webdriver.Chrome("E:/PyCharm Projects/chromedriver.exe")

    # Hitting site for Image to text conversion task
    driver.get('https://jinapdf.com/image-to-text-file.php')
    time.sleep(3)
    page = driver.page_source
    file_ = open('page.html', 'w', encoding='utf-8')
    file_.write(page)
    file_.close()

    #Upload Captcha Image file to the site for text conversion
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//input[@id="add-file-input"]').send_keys('E:/PyCharm Projects/Captcha_image.jpg')

    #Now click on download the converted text file from captcha image file.
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//div[@id="downloadfile"]').click()

    # Now open downloaded converted captcha text file and read it's content from Captcha Image file.
    source = os.listdir("C:/Users/Krishna Gupta/Downloads/")
    for files in source:
        if files.startswith("converted_"):
            file_path = "C:/Users/Krishna Gupta/Downloads/" + files
            file = open(file_path, "r")
            captcha_text = file.read()
    driver.quit()
    return captcha_text


def mainprogram():
    url="https://www.amazon.in/Airtel-4G-Hotspot-E5573Cs-609-Portable/dp/B06WV9WR4Z"
    time.sleep(7)
    response = get(url)
    resp=response.text
    with open("Prod_page.html", 'w', encoding='utf-8') as file:  # Writing Product Page
        file.write(resp)
    match_val=resp.find("Robot check") or resp.find("Robot Check") or resp.find("robot check")

    if match_val!= -1 or len(resp) < 12000:#Condition for captcha page
        print("Got Captcha Page...")
        cap_text = captch_Img_Text(resp)
        print("Captcha image to text value is: ", cap_text)
    else:
        print("Not Captcha Page...")

#Delete all downloaded text file converted from Captcha image file.
source = os.listdir("C:/Users/Krishna Gupta/Downloads/")
for files in source:
    if files.startswith("converted_"):
        file_path = "C:/Users/Krishna Gupta/Downloads/" + files
        os.remove(file_path)

def job():
    print("Getting Captcha Image file .... and convert it into a text file and print out the text.")
    mainprogram()

# main code
schedule.every(0.0).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)




