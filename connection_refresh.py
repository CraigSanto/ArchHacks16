from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time

driver = webdriver.Firefox()
print('sasa')
driver.get("file:///C:/Users/Craig/Documents/testmap.html")
#assert "Python" in driver.title
#elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
while 1:
	time.sleep(5)
	driver.refresh()
driver.close()
