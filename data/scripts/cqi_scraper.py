from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from io import StringIO
import time

# open chromedriver
driver = webdriver.Chrome()
time.sleep(2)

# navigate to arabic coffee
driver.get('https://database.coffeeinstitute.org/')
time.sleep(2)
driver.find_element(By.LINK_TEXT, "Q Arabica Coffees").click()
time.sleep(2)

# enter the max number of pages you see on the website
# make sure this is accurate, or it can break during scripting process
max_page = 8

# starts from the very first row of page 1
def switch_pages(desired):
    # get the paginate buttons grouping and individual elements
    paginate_buttons = driver.find_element(By.CLASS_NAME, "dataTables_paginate")

    # get the current page using paginate buttons grouping
    curr_page = paginate_buttons.find_element(By.CLASS_NAME, "current")

    if int(curr_page.text) == desired:
        return
    
    if (int(curr_page.text) <= 4 and (desired > 4 and desired < max_page)):
        paginate_buttons.find_element(By.LINK_TEXT, "5").click()
        time.sleep(5)
        switch_pages(desired)
    elif (int(curr_page.text) > 4 and (desired <= 4 and desired > 1)):
        paginate_buttons.find_element(By.LINK_TEXT, "4").click()
        time.sleep(5)
        switch_pages(desired)
    else:
        paginate_buttons.find_element(By.LINK_TEXT, str(desired)).click()
        time.sleep(5)
        return

# helps resume you if the parser breaks 
# default is page 1, row 1
begin_page = 6

# tracks the current page you're on
for curr_page in range(begin_page, (max_page + 1)):
    # loops through all the rows
    for curr_row in range(1, 51):
        # switch to the page of choice
        switch_pages(curr_page)

        print("Current page: " + driver.find_element(By.CLASS_NAME, "dataTables_paginate").find_element(By.CLASS_NAME, "current").text)
        print("Current row: " + str(curr_row))

        # once the table has switch, copy the table to start scrapping
        data_table = driver.find_element(By.CLASS_NAME, "cqi_data")

        # click on the link that corresponds to curr_row
        try:
            row_element = "tbody > tr:nth-child(" + str(curr_row) + ")"
            data_row = data_table.find_element(By.CSS_SELECTOR, row_element).find_element(By.TAG_NAME, "a").click()
            time.sleep(5)

            # get all the tables with the sample info
            info_tables = driver.find_elements(By.CLASS_NAME, "sample_information")
            print("num of tables: " + str(len(info_tables)))

            # prep for labeling csv files
            table_num = 0

            # parse the tables into the individual csv
            for table in info_tables:
                t = table.get_attribute('outerHTML')
                # Wrap the HTML string in a StringIO object
                html_io = StringIO(t)
                df = pd.read_html(html_io)
                name = 'scraped_data/coffee_pg{}_row{}_table{}.csv'.format(curr_page,curr_row,table_num)
                df[0].to_csv(name)
                print(name)

                table_num += 1
            
            print()
            # go back to the previous page
            driver.back()
            time.sleep(5)
        except:
            print("Either error with getting row data, or no more rows to scrape!")
            break

# done!
driver.close()


                  






	


	



