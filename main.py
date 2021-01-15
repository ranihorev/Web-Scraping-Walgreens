
from city_stores import scrape_all_cities
from allcities import scrape_cities
from selenium import webdriver

def scrape():
    driver=webdriver.Chrome(executable_path='./chromedriver')
    cities = scrape_cities(driver)
    print(cities)
    scrape_all_cities(cities)
    
if __name__ == "__main__":
    scrape()