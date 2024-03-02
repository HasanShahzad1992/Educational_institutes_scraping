import selenium.webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


driver_path="C:/Users/Admin/Desktop/pythonpractice/chromedriver.exe"
driver=wd.Chrome(executable_path=driver_path)
wait=WebDriverWait(driver,10)
link_list=[]
list_location_search=["Coaching Center Mingora Pakistan","institute mingora pakistan","academy mingora pakistan","Coaching Center Mardan Pakistan","institute mardan pakistan","academy mardan pakistan","Coaching Center Mansehra Pakistan","institute Mansehra pakistan","academy Mansehra pakistan","Coaching Center hangu Pakistan","institute hangu pakistan","academy hangu pakistan","Coaching Center bannu Pakistan","institute bannu pakistan","academy bannu pakistan","Coaching Center batkhela Pakistan","institute batkhela pakistan","academy batkhela pakistan","Coaching Center karak Pakistan","institute karak pakistan","academy karak pakistan","Coaching Center chitral Pakistan","institute chitral pakistan","academy chitral pakistan","Coaching Center haripur Pakistan","institute haripur pakistan","academy haripur pakistan","Coaching Center Tordher Pakistan","institute Tordher pakistan","academy Tordher pakistan"]
for i in list_location_search:
    driver.get("https://www.google.com/maps")
    wait=WebDriverWait(driver,10)
    target_search_box=wait.until(EC.presence_of_element_located((By.ID,"searchboxinput")))
    target_search_box.send_keys(i)
    target_search_icon=wait.until(EC.element_to_be_clickable((By.ID,"searchbox-searchbutton")))
    target_search_icon.click()
    time.sleep(4)
    target_sidebar=wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]")))
    while True:
        current_scroll_position = driver.execute_script("return arguments[0].scrollTop", target_sidebar)

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", target_sidebar)

        time.sleep(1)

        new_scroll_position = driver.execute_script("return arguments[0].scrollTop", target_sidebar)
        time.sleep(3)
        if new_scroll_position == current_scroll_position:
            break
    time.sleep(10)
    target_coaching_centers_link=wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"hfpxzc")))
    for i in target_coaching_centers_link:
        try:
            target_coaching_centers_link=i.get_attribute("href")
            link_list.append(target_coaching_centers_link)
            time.sleep(1)
        except:
            print("not found")
print(link_list)



list_necessary_information=[]
coaching_name_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1"
coaching_type_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]"
coaching_status_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[4]/div[1]/div[2]/div/span[1]"



for i in link_list:
    driver.get(i)
    try:
        coaching_center_element=wait.until(EC.presence_of_element_located((By.XPATH,coaching_name_xpath)))
        coaching_center_name_text=coaching_center_element.text
    except:
        coaching_center_name_text="Not found"
    try:
        category_of_institute_element=wait.until(EC.presence_of_element_located((By.XPATH,coaching_type_xpath)))
        category_of_institute=category_of_institute_element.text
    except:
        category_of_institute="Not found"
    try:

        status_open_close_element=wait.until(EC.presence_of_element_located((By.XPATH,coaching_status_xpath)))
        status_open_close=status_open_close_element.text
    except:
        status_open_close="Not found"
    try:
        def scroll_sidebar_to_bottom():
            sidebar = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]")))
            driver.execute_script("arguments[0].scrollTop += 50", sidebar)
        for i in range(4):
            scroll_sidebar_to_bottom()
        time.sleep(5)
        phone_element=wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Io6YTe')))

        text_list = []
        for address_element in phone_element:
            address_text = address_element.text
            text_list.append(address_text)
    except:
        phone_text="Not found"

    list_necessary_information.append([coaching_center_name_text,category_of_institute,status_open_close] + text_list)
    print(text_list)

    # print([coaching_center_name_text,category_of_institute,address,status_open_close,phone_text])
data_frame = pd.DataFrame(list_necessary_information)
data_frame.to_excel("institutions_information.xlsx")