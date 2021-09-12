from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from pandas import DataFrame
import time

url="https://trip.com"
chrome_driver_path="chromedriver.exe"

if __name__=="__main__":
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(10)  
    

destination = driver.find_element(By.ID,"hotels-destination")
destination.send_keys("Beijing")
time.sleep(5)



destination = driver.find_element(By.ID,"hotels-destination")
destination.send_keys("Beijing")
time.sleep(5)


# by default check in: today's date
# Below snipit selects any date checkin or checkout
checkin_date = driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[2]/div/div[1]/input")
checkin_date.click()



#print(checkin_date.get_attribute("value"))
current_checkin_date_on_chart=checkin_date.get_attribute("value")
print('Checkin date:',current_checkin_date_on_chart)


# Below snipit selects date
current_month = driver.find_elements(By.CLASS_NAME,"c-calendar-month__days")
all_dates = current_month[0].find_elements(By.TAG_NAME,"li")
for date in all_dates:
    if (date.text) == '15' and date.get_attribute("class") != 'is_disable':
        date.click()
        print("breaking the loop")
        break;
    print(date.text,date.get_attribute("class"))
    
    
    
# Below snipit selects month    
date_displayed_on_calendar = driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[2]/div/div[4]/div/div[1]/div[1]/h3")
date_string = date_displayed_on_calendar.text
month_string,year_string = date_string.split(" ")
print(month_string,year_string)
if current_checkin_date_on_chart.find(month_string) != -1:
    driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[2]/div/div[4]/div/div[1]/span[2]").click()
    #block found
else:
    print("string not found")   
    
    
# created select_date function which returns check-in & check-out Dates    
def select_date(driver,formated_date,xpath_of_date_to_be_clicked):
    '''xpath_of_date_to_be_clicked Check-In or Check-Out'''
    '''expected date in format Sat, Jun 13'''
    '''NOTE TRIP.COM DOESNOT ALLOW US TO EXCEED 28 days'''
    MONTHS_IN_A_YEAR = 12
    #shifting focus on calander pre_selected_dates
    pre_selected_date = driver.find_element(By.XPATH,xpath_of_date_to_be_clicked)
    pre_selected_date.click()
    #getting user_weekday = 'Sat' and user_month_and_date=' June 13'
    user_weekday,user_month_and_date = formated_date.split(",")
    #getting user_month='June' and user_date='13'
    user_month,user_date = user_month_and_date.lstrip().split(" ")
    month_found = False
    #traversing month if not found
    for _ in range(MONTHS_IN_A_YEAR):
        month_and_year_inside_calander_pop_up = driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[2]/div/div[4]/div/div[1]/div[1]/h3")
        month_and_year_inside_calander_pop_up_str = month_and_year_inside_calander_pop_up.text
        #getting selected_month='June' and selected_year='2020'
        selected_month,selected_year = month_and_year_inside_calander_pop_up_str.split(" ")
        if selected_month != user_month:
            #move to next month
            print("moving on to the next month")
            driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[2]/div/div[4]/div/div[1]/span[2]").click()
            #pre_selected_date.click()
            continue
        else :
            month_found = True
            break
    if month_found != True:
        raise ValueError("Month not found") 
    INDEX_OF_LHS_MONTH_BOX = 0
    #getting both month boxes being displayed
    current_month = driver.find_elements(By.CLASS_NAME,"c-calendar-month__days")
    all_dates = current_month[INDEX_OF_LHS_MONTH_BOX].find_elements(By.TAG_NAME,"li")
    date_found = False
    for date in all_dates:
        if (date.text) == user_date and date.get_attribute("class") != 'is_disable':
            date.click()
            date_found = True
            print("breaking the loop")
            break;
        print(date.text,date.get_attribute("class"))
    if date_found != True:
        raise ValueError("date not found")    
    #print(date,month,weekday)
#time.sleep(5)    
select_date(driver,'Web, Nov 18',"//*[@id='searchBoxCon']/div/div/ul/li[2]/div/div[1]/input")
#time.sleep(5)
select_date(driver,'Web, Nov 25',"//*[@id='searchBoxCon']/div/div/ul/li[2]/div/div[3]/input")



# created set_rooms_and_guest function which returns no. of rooms, no. of adults & no. of childrens
def set_rooms_and_guest(driver,no_rooms,no_adults,no_children):
    '''NOTE rooms should not exceed adults'''
    room_block = driver.find_element(By.CLASS_NAME,'room-guest-container')
    room_block.click() 
    time.sleep(1)
    try:
        driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[3]/div/div[3]/div[1]/div/span[3]/i")
    except NoSuchElementException as err:
        room_block.click()
        print("button is clicked again")
        time.sleep(1)
    #time.sleep(1)
    rooms_feed_btn = driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[3]/div/div[3]/div[1]/div/span[3]/i")
    adults_feed_btn = driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[3]/div/div[3]/div[2]/div/span[3]/i")
    child_feed_btn = driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[3]/div/div[3]/div[3]/div/span[3]/i")
    spin = max(no_rooms,no_adults,no_children)
    for i in range(spin):
        if i < (no_adults - 1):
            adults_feed_btn.click()
        if i < (no_children):
            child_feed_btn.click()
        if i <  (no_rooms - 1):
            rooms_feed_btn.click()
            
    driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[3]/div/div[3]/div[4]/span").click()
set_rooms_and_guest(driver,1,2,0)



driver.find_element(By.XPATH,"//*[@id='searchBoxCon']/div/div/ul/li[5]/div/i").click()


card_items = driver.find_elements(By.CLASS_NAME,"hotel-info")
print(len(card_items))
lst_real_price =[]
lst_hotel_name=[]
lst_number_of_stars=[]
df = pd.DataFrame()


#hotel_name=""
for card_item in card_items:
    real_price = ""
    hotel_name = ""
    number_of_stars = 0
    print(card_item.text)
    df = lst_hotel_name
    lst_hotel_name.append(card_item.text)
    

df = pd.DataFrame(df)
df.to_excel("output.xlsx")
 #print(df)