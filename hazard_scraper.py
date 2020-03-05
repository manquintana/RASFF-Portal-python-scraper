
# This is a Py Scraper to obtain the correlation between Substance Hazard Category and Subject from the RASFF Portal #
# Manuel Quintana 3/3/20


#Strategy: obtener de las tablas de todas las paginas todos los REFERENCE de https://webgate.ec.europa.eu/rasff-window/portal/# tras apretar GET RESULTS
#after that, execute https://webgate.ec.europa.eu/rasff-window/portal/?event=notificationDetail&NOTIF_REFERENCE=2020.0999 cambiando el REFERENCE POR CADA REFERENCE OBTENIDO. AHI ESTA TODA LA DATA

from pandas.io.html import read_html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import math
import pandas as pd
import time

driver = webdriver.Chrome(executable_path='/home/manuel/3. git/RASFF_portal_python_scrapper/chromedriver')
driver.get('https://webgate.ec.europa.eu/rasff-window/portal/#')

datos = pd.DataFrame(columns=['Reference','Subject','HazardCategory'])
  
get_results = driver.find_element_by_id("Btn_Search")
get_results.click()

titles = driver.find_elements_by_xpath('//h1')
wanted_title = titles[1].text #The second h1 has the number of results
numbs = [int(s) for s in wanted_title.split() if s.isdigit()] #Extracting numbers from string
results_number = numbs[0]
print('Cantidad de resultados: {0}'.format(results_number))


# #########################################################
# PART 1: GETTING REFERENCE CODES FROM ALL PAGES OF RESULTS
# #########################################################
reference_codes = []
subjects = []
hazards = []
current_page = 0
total_pages = math.ceil(results_number/100)

while(results_number > 0):
    current_page = current_page + 1 
    #print('Agregando codigos de la pagina {0} de {1}'.format(current_page, total_pages))
    rows = driver.find_elements_by_xpath('//tr') #selecting rows from table

    for i in range(1,len(rows)):
        print('>>>')
        print('Agregando codigos de la pagina {0} de {1}'.format(current_page, total_pages))
        columns = rows[i].find_elements_by_css_selector("td")
        current_reference_code = columns[3].text
        current_subject = columns[5].text\
        
        #print(current_reference_code)
        #print(current_subject)
        
        details_link = 'https://webgate.ec.europa.eu/rasff-window/portal/?event=notificationDetail&NOTIF_REFERENCE='+current_reference_code #Acceder a details para cada row!
        get_link = driver.find_element_by_xpath('//a[@href="'+details_link+'"]')
        get_link.click()
               
        driver.switch_to.window(driver.window_handles[1])  #Access to new tab
        #recuperar los hazards y guardar todo en un data frame
        time.sleep(2)
        hazards = driver.find_elements_by_xpath('//*[@id="hazards"]/tbody/tr') #selecting rows from table
        temp_list = []
        for h in hazards:
            hazard_columns = h.find_elements_by_css_selector("td")
            #print(hazard_columns[1].text)
            temp_list.append(hazard_columns[1].text)
        #print('  ')
        deduplicate = list(set(temp_list))
        for haz in deduplicate:
            temp_df = pd.DataFrame({'Reference':[current_reference_code],'Subject':[current_subject],'HazardCategory':[haz]})
            datos = datos.append(temp_df, ignore_index = True)
            #print('Data already scrapped:')
            #print(datos)    
            
        driver.close() #Close new tab
        driver.switch_to.window(driver.window_handles[0]) #return to original tab

    results_number = results_number - 100
    print('Data scrapped:')
    print(datos)   
    if results_number > 0: #hay que seguir scrapeando!
        next_page = driver.find_element_by_link_text("Next 100")
        next_page.click()
    #Ya levante toda la data de la pagina actual


print('All the data has been scrapped! Saving to file datascrapped.csv')
datos.to_csv('datascrapped.csv')
