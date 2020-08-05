from selenium import webdriver
import sys
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait


driver = webdriver.Chrome()
driver.get("https://www.piac.com.pk/#schedules")

close_popup = driver.find_element_by_id("popup").click()

print("\n****************************** DEPARTURE CITIES ********************************\n")
select_box_departure = driver.find_element_by_name("depPort") 
options = [x for x in select_box_departure.find_elements_by_tag_name("option")]
for element in options:
    # dep_city_value = element.get_attribute("value")
    dep_city_text = element.text
    print (dep_city_text)
    
print('\nEnter Departure City From Any Of Above:')
departure = input()

departure_select_element = driver.find_element_by_xpath("/html/body/section/div[1]/div[2]/div/div/div/div/div[2]/form/div[1]/div[1]/div[1]")
departure_select_element.click()

departure_search_element = driver.find_element_by_xpath("/html/body/span/span/span[1]/input")
departure_search_element.send_keys(departure)
departure_search_element.send_keys(Keys.RETURN)

sleep(2)

print("\n****************************** ARRIVAL CITIES ********************************\n")
select_box_arrival = driver.find_element_by_name("arrPort") 
options = [x for x in select_box_arrival.find_elements_by_tag_name("option")]
for element in options:
    # dep_city_value = element.get_attribute("value")
    arr_city_text = element.text
    print (arr_city_text)

print('\nEnter Destination/Arrival City From Any Of Above:')
destination = input()

arrival_select_element = driver.find_element_by_xpath("/html/body/section/div[1]/div[2]/div/div/div/div/div[2]/form/div[1]/div[1]/div[2]")
arrival_select_element.click()

arrival_search_element = driver.find_element_by_xpath("/html/body/span/span/span[1]/input")
arrival_search_element.send_keys(destination)
arrival_search_element.send_keys(Keys.RETURN)

# sleep(2)

print("\n****************************** DEPARTURE DATE ********************************\n")

print('Enter Departure Date: (Format: dd/mm/yyyy)')
departure_date = input()
departure_date = departure_date.split("/")
day = departure_date[0]
month = departure_date[1]
year = departure_date[2]

# print(day)
# print(month)
# print(year)

sleep(2)
date_element = driver.find_element_by_id("dpd3").click()
select_month = Select(driver.find_element_by_class_name("ui-datepicker-month"))
select_month.select_by_value(str(int(month)-1))

days_element = driver.find_element_by_class_name("ui-datepicker-calendar")
day_elements = days_element.find_elements_by_tag_name("td")

for day_element in day_elements:
    # print(day_element.text)
    site_day = day_element.text
    # print(site_day)

    try:
        if int(day) == int(site_day):
            print("Proceeding.....")
            day_element.click()
            break

            # Testing Data
            # Lahore - Allama Iqbal Intl. (LHE)
            # Manchester (MAN)
            # 11/12/2020

    except Exception:
        pass

proceed = driver.find_element_by_xpath("//*[@class='btn btn-primary pull-right submit-btn']")
proceed.click()
sleep(4)

departure_time = driver.find_element_by_xpath("/html/body/form/div[2]/div/div/div[4]/div[6]/table/tbody/tr/td[1]").text
departure_day_date = driver.find_element_by_xpath("/html/body/form/div[2]/div/div/div[4]/div[6]/table/thead/tr/th[2]").text
departure_day_date = departure_day_date.split("\n")
departure_day = departure_day_date[0]
departure_date = departure_day_date[1]
# departure_flightNo = driver.find_element_by_xpath("/html/body/form/div[2]/div/div/div[4]/div[6]/table/tbody/tr/td[2]/div/div[2]/a/span").get_attribute("innerHTML")
departure_flightNo = driver.find_element_by_class_name("modal-side-links").get_attribute("innerHTML")

radio_btn = driver.find_element_by_xpath("/html/body/form/div[2]/div/div/div[4]/div[6]/table/tbody/tr/td[2]/div/div[1]/div")
radio_btn.click()
# driver.find_element_by_css_selector("input[type='radio'][value='SRF']").click()

oneway_flight_search = driver.find_element_by_id("btnSearch_0")
oneway_flight_search.click()
sleep(4)

departure_flight_info = driver.find_element_by_xpath("/html/body/form/div[4]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[4]/div[1]/div[4]").text
departure_economy_ticket_price = driver.find_element_by_xpath("/html/body/form/div[4]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[4]/div[2]/div[1]/div/a/div[2]/span[1]").get_attribute("innerHTML")
departure_executive_economy_ticket_price = driver.find_element_by_xpath("/html/body/form/div[4]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[4]/div[2]/div[2]/div/a/div[2]/span[1]").get_attribute("innerHTML")
departure_business_ticket_price = driver.find_element_by_xpath("/html/body/form/div[4]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[4]/div[2]/div[3]/div/span").get_attribute("innerHTML")


print("\n****************************** Cabin ********************************\n")
print("Economy")
print("Executive Economy")
print("Business")

print('\nEnter Cabin\Class From Any Of Above:')
cabin = input()

if cabin == 'Economy':
    select = driver.find_element_by_xpath("/html/body/form/div[4]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[4]/div[2]/div[1]/div")
    select.click()

if cabin == 'Executive Economy':
    select = driver.find_element_by_xpath("/html/body/form/div[4]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[4]/div[2]/div[2]/div")
    select.click()

if cabin == 'Business':
    select = driver.find_element_by_xpath("/html/body/form/div[4]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[4]/div[2]/div[3]/div")
    select.click()

sleep(2)


print("\n****************************** Information ********************************\n")

print("departure_time: " + departure_time)
print("departure_day: " + departure_day)
print("departure_date: " + departure_date)
print("departure_flightNo: " + departure_flightNo)
print("departure_flight_info: " + departure_flight_info)
print("departure_economy_ticket_price: " + departure_economy_ticket_price)
print("departure_executive_economy_ticket_price: " + departure_executive_economy_ticket_price)
print("departure_business_ticket_price: " + departure_business_ticket_price)

print("\n****************************** further_info ********************************\n")

further_info = driver.find_element_by_xpath("//*[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12 basket-summary']").text
print(further_info)

print("*******************************************************************************")




sleep(25)
driver.quit()
    






# action = ActionChains(driver)
# departure_cities_arrow_down = driver.find_element_by_xpath("/html/body/section/div[1]/div[2]/div/div/div/div/div[2]/form/div[1]/div[1]/div[1]/span/span[1]/span/span[2]")
# action.move_to_element(departure_cities_arrow_down).perform().click()
# departure_cities_arrow_down.click()

# wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='From: Airport & City']"))).click()

# print("clicked")
