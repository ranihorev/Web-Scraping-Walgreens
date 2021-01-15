from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

#using allstate.py
allurl=['http:/www.walgreens.com/storelistings/storesbycity.jsp?requestType=locator&state=CA']

def scrape_cities(driver):
	all_cities_links=[]
	count1=0
	for i in allurl:
		count=0
		driver.get(i)
		delay = 3 # seconds
		try:
			myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))

			
		except TimeoutException:
			pass

			

		# res=requests.get("https://www.walgreens.com/storelocator/find.jsp?requestType=locator&state=IL&city=ADDISON&from=localSearch")

		res=driver.execute_script("return document.documentElement.outerHTML")

		soup=bs(res,'html.parser')
		box=soup.findAll(class_="row")
		for div in box:
			links = div.findAll('a')
			for a in links:
				if(len(a['href'])>3):
					count+=1
					b="http:/www.walgreens.com"+a['href']
					all_cities_links.append(b)
		count1+=count
		print(i[-2:]+" "+str(count))
	return all_cities_links

if __name__ == "__main__":
	driver=webdriver.Chrome(executable_path='./chromedriver')
	print(scrape_cities(driver))