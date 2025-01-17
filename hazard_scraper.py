
# This is a Py Scraper to obtain the correlation between Substance Hazard Category and Subject 
# from the RASFF Portal for the European Comission #
# Manuel Quintana 3/3/20


#Strategy: obtener de las tablas de todas las paginas todos los REFERENCE de https://webgate.ec.europa.eu/rasff-window/portal/# tras apretar GET RESULTS
#after that, execute https://webgate.ec.europa.eu/rasff-window/portal/?event=notificationDetail&NOTIF_REFERENCE=2020.0999 cambiando el REFERENCE POR CADA REFERENCE de la pagina actual (cada row)

from pandas.io.html import read_html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import math
import pandas as pd
import time
import sqlalchemy

# Local DB
DB_USER = '.....'
DB_PASS = '.....'
DB_ADDR = 'localhost'
DB_NAME = 'rasff_hazards'
DB_CONN = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(DB_USER, DB_PASS, DB_ADDR, DB_NAME))


driver = webdriver.Chrome(executable_path='/home/manuel/3. git/RASFF_portal_python_scrapper/chromedriver')
driver.get('https://webgate.ec.europa.eu/rasff-window/portal/#')

  
get_results = driver.find_element_by_id("Btn_Search")
get_results.click()

titles = driver.find_elements_by_xpath('//h1')
wanted_title = titles[1].text #The second h1 has the number of results
numbs = [int(s) for s in wanted_title.split() if s.isdigit()] #Extracting numbers from string
results_number = numbs[0]
print('Cantidad de resultados: {0}'.format(results_number))

def append_to_table(data, table_name):
    print('| Updating table: ' + table_name + '...')
    total_rows= len(data)
    for i in range(total_rows):
        try:
            print ("| Appending row #" + str(i+1) + " of " + str(total_rows))
            data.iloc[i:i+1].to_sql(con=DB_CONN, name='subject_hazard', if_exists='append', index = False)
        except:
            print("| >> Data Error" + str(i+1))
            print('| Content with error: ' + data.iloc[i:i+1])
    print(' ')
    print(' ')

# #########################################################
# PART 1: GETTING REFERENCE CODES FROM ALL PAGES OF RESULTS
# #########################################################
reference_codes = []
subjects = []
hazards = []
current_page = 0
total_pages = math.ceil(results_number/100)

#Restore after error!!!
error_page= 0 #Set error_page = 0 if not error, to scrapp from the beginning!!
for i in range(1,error_page):
    #time.sleep(1.5)
    results_number = results_number - 100
    current_page = current_page + 1 
    next_page = driver.find_element_by_link_text("Next 100")
    next_page.click()

while(results_number > 0):
    time.sleep(1)
    current_page = current_page + 1 
    rows = driver.find_elements_by_xpath('//tr') #selecting rows from table
    
    print('>>>')
    print('Agregando codigos de la pagina {0} de {1}'.format(current_page, total_pages))
    datos = pd.DataFrame(columns=['Reference','Subject','HazardCategory'])

    for i in range(1,len(rows)):
        columns = rows[i].find_elements_by_css_selector("td")
        current_reference_code = columns[3].text
        current_subject = columns[5].text
        
        details_link = 'https://webgate.ec.europa.eu/rasff-window/portal/?event=notificationDetail&NOTIF_REFERENCE='+current_reference_code #Acceder a details para cada row!
        get_link = driver.find_element_by_xpath('//a[@href="'+details_link+'"]')
        get_link.click()
               
        driver.switch_to.window(driver.window_handles[1])  #Access to new tab
        #Recover hazards and load them into a dataframe
        time.sleep(2)
        hazards = driver.find_elements_by_xpath('//*[@id="hazards"]/tbody/tr') #selecting rows from table
        temp_list = []
        for h in hazards:
            hazard_columns = h.find_elements_by_css_selector("td")
            #print(hazard_columns[1].text)
            temp_list.append(hazard_columns[1].text)
        deduplicate = list(set(temp_list))
        for haz in deduplicate:
            temp_df = pd.DataFrame({'Reference':[current_reference_code],'Subject':[current_subject],'HazardCategory':[haz]})
            datos = datos.append(temp_df, ignore_index = True)
            
        driver.close() # Close new tab
        driver.switch_to.window(driver.window_handles[0]) # Return to original tab

    # Persist data
    print('Data scrapped:')
    print(datos)
    print('Saving data to Database')
    datos.rename(columns = {'Reference':'reference', 'Subject':'subject', 'HazardCategory':'hazard_category'}, inplace = True) 
    append_to_table(datos, 'subject_hazard')
    
    results_number = results_number - 100
    if results_number > 0: # There are more pages to scrap!
        time.sleep(1.5)
        next_page = driver.find_element_by_link_text("Next 100")
        next_page.click()

print('The End!')
