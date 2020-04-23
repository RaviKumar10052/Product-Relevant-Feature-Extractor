# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

import process_raw_review_data
import pos_tag_reviews
import feature_list_extraction
import analyse_processed_data
class Scrap(unittest.TestCase):
    def setUp(self):
        #self.driver = webdriver.Firefox()

        self.link = input("Enter the Link: ")
        self.f = open("review.txt", "w")
        self.driver = webdriver.Chrome(executable_path="/home/ravi/PycharmProjects/Major2V2/drivers/chromedriver")
        #self.driver = webdriver.Firefox(executable_path="/home/ravi/PycharmProjects/Major2V2/drivers/chromedriver")
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.driver.maximize_window()
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_major2(self):
        f = self.f
        driver = self.driver
        # driver.get("https://www.amazon.in/")
        # driver.find_element_by_id("twotabsearchtextbox").click()
        # driver.find_element_by_id("twotabsearchtextbox").clear()
        # driver.find_element_by_id("twotabsearchtextbox").send_keys(self.product)
        # f.write("product/productId:" + (str)(self.product) + "\n")
        # driver.find_element_by_name("site-search").submit()
        #
        # driver.find_element_by_xpath("//div[@data-index= '1']//child::a[@class='a-link-normal a-text-normal'][1]").click()
        # # driver.find_element_by_xpath("//div[@id='customer_review-R3RV7C7RVVZ3WS']/div[4]/span/div/div").click()
        # driver.switch_to_window(driver.window_handles[1])
        driver.get(self.link)

        product = driver.find_element_by_xpath("//div[@id='prodDetails']//div[2]//div[1]//div[2]//div[1]//div[1]//following::td[@class='value']").text
        f.write("product/productId:" + product + "\n")

        productName = driver.find_element_by_id("productTitle").text
        f.write("product/name:" + (str)(productName) + "\n")

        # while (True):
        #     try:
        #         print("Before click")
        #         driver.find_element_by_xpath("//div[@class='a-section a-spacing-top-extra-large']//input[@class='a-button-input']").click()
        #         print("After click")
        #     except NoSuchElementException:
        #         break

        # driver.execute_script("window.scrollTo(0, 1020);")
        time.sleep(2)
        ele = driver.find_elements_by_xpath("//div[@data-hook = 'review-collapsed']/span")
        for e in ele:
            txt = " ".join((e.text).split())
            if txt == " " or txt == "":
                continue
            f.write("review/text:" + str(txt) + "\n")


    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.f.close()
        self.driver.quit()
        process_raw_review_data.main()
        pos_tag_reviews.main()
        feature_list_extraction.main()
        analyse_processed_data.main()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
