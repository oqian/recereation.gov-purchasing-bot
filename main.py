# Author: Oliver Qian
# For personal use only, not for commercial use
# MIT Licence
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import json

def json_parsing():
    """
    :param file:
    {email: email address,
     password: login password
     date:MM/DD/YYYY,
     firstName: firstName,
     lastName: lastName,
     cardNumber: credit card number,
     Month: credit card expiration month (MM),
     Year: credit card expiration year (YY),
     securityCode: CVV
    }
    :return:a dictionary of key-value pairs
    """
    with open("credentials.json") as f:
        data = json.load(f)
    return data



def make_selection(file: dict):
    browser = webdriver.Chrome(executable_path='./chromedriver.exe')
    browser.get('https://www.recreation.gov/timed-entry/10086910/ticket/10086911')
    browser.find_element_by_id('ga-global-nav-log-in-link').click()
    browser.find_element_by_id("email").send_keys(file['email'])
    browser.find_element_by_id("rec-acct-sign-in-password").send_keys(file['password'])
    browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div/div[2]/form/button").click()
    browser.find_element_by_id("tourCalendarWithKey").send_keys(file['date'])
    found = False
    count = 0
    while not found:
        count += 1
        time.sleep(4)
        for time_slot in range(2, 8):
            path = f"/html/body/div[1]/div/div[3]/main/div[3]/div/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div[3]/div/div/label[{time_slot}]"
            if browser.find_element_by_xpath(xpath=path).get_attribute("aria-describedby"):
                browser.find_element_by_xpath(xpath=path).click()
                found = True
                print("ticket found")
                break
        if not found:
            browser.get('https://www.recreation.gov/timed-entry/10086910/ticket/10086911')
            browser.find_element_by_id("tourCalendarWithKey").send_keys(file['date'])
            print(f"It is the {count} attempt, and no available ticket is found")

        if count == 5:
            quit()

    # request tickets
    browser.find_element_by_xpath(
        "/html/body/div[1]/div/div[3]/main/div[3]/div/div[1]/div[1]/div/div[3]/div[2]/button").click()
    time.sleep(1)
    while True:
        try:
            browser.find_element_by_xpath(
                "/html/body/div[1]/div/div[3]/main/div[3]/div[1]/div/div[1]/div/section[2]/div[3]/label").click()
            time.sleep(1)
            browser.find_element_by_xpath(
                "/html/body/div[1]/div/div[3]/main/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div/div[6]/button[1]").click()
            time.sleep(2)
            browser.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div/div/div/div[2]/div[1]/div[4]/button[1]").click()
            time.sleep(2)
            browser.find_element_by_xpath(
                "/html/body/div[1]/div/div[4]/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[1]/input").send_keys(
                "Yichi")
            browser.find_element_by_xpath(
                "/html/body/div[1]/div/div[4]/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/input").send_keys(
                "Qian")
            browser.find_element_by_xpath(
                "/html/body/div[1]/div/div[4]/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/input").send_keys(
                file['cardNumber'])
            select = Select(browser.find_element_by_xpath(
                "/html/body/div[1]/div/div[4]/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[3]/div[1]/select"))
            select.select_by_value(file['Month'])
            select2 = Select(browser.find_element_by_xpath(
                "/html/body/div[1]/div/div[4]/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[3]/div[2]/select"))
            select2.select_by_value(file['Year'])
            browser.find_element_by_xpath(
                "/html/body/div[1]/div/div[4]/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[4]/div/input").send_keys(file['securityCode'])
            browser.find_element_by_xpath(
                "/html/body/div[1]/div/div[4]/div/div/div/div[1]/div[2]/div[1]/div/div[2]/button").click()
            time.sleep(20)
            # browser.find_element_by_xpath(
            #     "/html/body/div[1]/div/div[4]/div/div/div/div[2]/div[2]/div[1]/div[4]/div[3]/button[2]").click()
            print("Successfully Purchased")
            break
        except selenium.common.exceptions.NoSuchElementException:
            print('not ready yet')
            time.sleep(5)


if __name__ == "__main__":
    file = json_parsing()
    make_selection(file)



