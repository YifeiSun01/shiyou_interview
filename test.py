import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import random

def get_currency_names_dict(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table', {"bordercolordark": "#ffffff"})
            currency_names_dict = {}
            for table in tables:
                for i in table.tbody.find_all('tr')[2:]:
                    td_list = i.find_all('td')
                    currency_names_dict[td_list[4].text.strip()] = td_list[1].text.strip()
            return currency_names_dict
        else:
            print(f"Failed to fetch HTML. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")
        return None

def get_foreign_exchange(date, currency_code,currency_names_dict,url,chrome_driver_path):
    currency_name = currency_names_dict[currency_code]
    date = str(date)
    year, month, day = date[:4],date[4:6],date[6:8]
    if month[0] == "0":
        month = month[1]
    if day[0] == "0":
        day = day[1]
    try:
        driver = webdriver.Chrome(service=Service(chrome_driver_path))
        try:
            driver.get(url)
            element = driver.find_element(By.ID, "erectDate")
            element.click()
            dropdown_year = Select(driver.find_element(By.ID, "calendarYear"))
            dropdown_year.select_by_value(str(year))
            dropdown_month = Select(driver.find_element(By.ID, "calendarMonth"))
            dropdown_month.select_by_value(str(int(month)-1))
            day_element = driver.find_element(By.XPATH, f"//table[@id='calendarTable']//td[text()='{day}']")
            day_element.click()
            element = driver.find_element(By.ID, "nothing")
            element.click()
            dropdown_year = Select(driver.find_element(By.ID, "calendarYear"))
            dropdown_year.select_by_value(str(year))
            dropdown_month = Select(driver.find_element(By.ID, "calendarMonth"))
            dropdown_month.select_by_value(str(int(month)-1))
            day_element = driver.find_element(By.XPATH, f"//table[@id='calendarTable']//td[text()='{day}']")
            day_element.click()
            dropdown_currency = Select(driver.find_element(By.ID, "pjname"))
            dropdown_currency.select_by_value(currency_name)
            search_button = driver.find_element(By.XPATH, "//input[contains(@class, 'search_btn') and contains(@style, 'float:right;margin-righth:26px;')]")
            search_button.click()
            time.sleep(3)
            try:
                tr_list = BeautifulSoup(driver.find_element(By.XPATH, "//table[contains(@cellpadding, '0') and contains(@cellspacing, '0') and contains(@align, 'left')]").get_attribute("innerHTML"), 'html.parser').find_all("tr")
                randint = random.randint(0,len(tr_list)-1)
                value = float(tr_list[randint+1].find_all("td")[3].text)
                driver.close()
                return value
            except:
                print("Can not acces this value")
        except:
            print("Can not access this URL")
    except:
        print("Can not launch Chrome Driver")

def write_to_file(data):
    with open("results.txt", "a") as file:
        file.write(data + "\n")

if __name__ == "__main__":
    url_1 = "https://www.11meigui.com/tools/currency"
    currency_names_dict = get_currency_names_dict(url_1)
    url_2 = "https://www.boc.cn/sourcedb/whpj/"
    chrome_driver_path = r"D:/Study/2024 winter/工作申请/公司/世游/chromedriver-win64/chromedriver.exe"
    for (date, currency_code) in [(20211231, "USD"),(20211112, "USD")]:
        value = get_foreign_exchange(date, currency_code,currency_names_dict,url_2,chrome_driver_path)
        data = f"{date}, {currency_code}, {value}"
        write_to_file(data)
