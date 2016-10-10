from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as bs
from settings import TEST_SITE
"""
Starting firefox
  sudo Xvfb :10 -ac
  export DISPLAY=:10
  firefox &


"""
browser = webdriver.Firefox()

browser.get(TEST_SITE)

assert 'Enlighted CRM - Test Site' in browser.title

p = browser.find_element_by_tag_name("h1")

assert p.text == 'Please Log In'
elem = browser.find_element_by_name('username')  # Find the search box
elem.send_keys('crm')
elem = browser.find_element_by_name('password')  # Find the search box
elem.send_keys('crmpass')
elem.send_keys(Keys.RETURN)


#print browser.page_source
#p = browser.find_element_by_tag_name("h1")
#assert p.text == 'Return Merchandise Authorizations'
# test search for abbvie
#element = WebDriverWait(browser, 20).until(
#        EC.presence_of_element_located((By.ID, "find-rma-by-customer-input")))
browser.implicitly_wait(10)
elem = browser.find_element_by_name('find-rma-by-customer-input')  # Find the search box
elem.send_keys('abb')

existing_rma_company = browser.find_element_by_id("rma-company_name-1805")
bspage = bs(existing_rma_company.get_attribute('innerHTML'))

anchs = bspage.findAll('a')
assert anchs[0].text == "Abbot Labs"

print (TEST_SITE.replace('\/crm_test', '')+anchs[0]['href'])
browser.get(TEST_SITE.replace('\/crm_test', '')+anchs[0]['href'])
browser.implicitly_wait(30)
#browser.quit()