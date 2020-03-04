
# This is a Py Scraper to obtain the correlation between Substance Hazard and Subject from the RASFF Portal #
# Manuel Quintana 3/3/20


#Strategy: obtener de las tablas de todas las paginas todos los REFERENCE de https://webgate.ec.europa.eu/rasff-window/portal/# tras apretar GET RESULTS
#after that, execute https://webgate.ec.europa.eu/rasff-window/portal/?event=notificationDetail&NOTIF_REFERENCE=2020.0999 cambiando el REFERENCE POR CADA REFERENCE OBTENIDO. AHI ESTA TODA LA DATA

from pandas.io.html import read_html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import math
import pandas as pd
import time

#driver = webdriver.Chrome()
driver = webdriver.Chrome(executable_path='/home/manuel/3. git/RASFF_portal_python_scrapper/chromedriver')
driver.get('https://webgate.ec.europa.eu/rasff-window/portal/#')


#df = pd.DataFrame(data, columns=['Reference','Subject','Hazard'])
#print (df)

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
    print('Agregando codigos de la pagina {0} de {1}'.format(current_page, total_pages))
    rows = driver.find_elements_by_xpath('//tr') #selecting rows from table
    #print(type(rows[1]))
    
    #print(len(rows))
    for i in range(1,len(rows)):
        columns = rows[i].find_elements_by_css_selector("td")
        current_reference_code = columns[3].text
        current_subject_code = columns[5].text
        #current_details = columns[9]
        
        print(current_reference_code)
        print(current_subject_code)
        #print(current_details)


        details_link = 'https://webgate.ec.europa.eu/rasff-window/portal/?event=notificationDetail&NOTIF_REFERENCE='+current_reference_code #Acceder a details para cada row!
        get_link = driver.find_element_by_xpath('//a[@href="'+details_link+'"]')
        get_link.click()
        
       
        driver.switch_to.window(driver.window_handles[1])  #Access to new tab
        #print("entre!!")
        #recuperar los hazards yguardar todo en un data frame
        time.sleep(2)
        hazards = driver.find_elements_by_xpath('//*[@id="hazards"]/tbody/tr') #selecting rows from table
        for h in hazards:
            #print(h.text)
            hazard_columns = h.find_elements_by_css_selector("td")
            print(hazard_columns[0].text)
        print('  ')
        #hazards = driver.find_elements_by_xpath('//tr') #selecting rows from table
        # for j in range(1,len(hazards)):
        #     hazard_columns = hazards[j].find_elements_by_css_selector("td")
        #     print(hazard_columns[0].text)
        #time.sleep(3)
       
        driver.close() #Close new tab
       
        driver.switch_to.window(driver.window_handles[0]) #return to original tab


        #print(current_details.text)
        #details_link = 'https://webgate.ec.europa.eu/rasff-window/portal/?event=notificationDetail&NOTIF_REFERENCE='+current_reference_code #Acceder a details para cada row!
        #get_link = driver.find_element_by_tag_name("a href="+details_link)
        #get_link.click()
        
        
        
    for a in results_table:
        ##### 1st. Get reference code
        reference_code = a[3]  
        reference_codes.append(reference_code)
        ##### 2nd. Get subject
        subject = a[5]
        subjects.append(subject)
        ##### 3rd. Get hazard (from the linked page)
        
        ## DIRECTAMENTE AGREGAR LOS 3 AL DATA FRAME, NO A LA LISTA REFERENCE CODES NI SUBJECTS,,, HAY CASOS DONDE HAY MAS DE UN HAZARD POR PRODUCTO!!!!!



    
    results_number = results_number - 100
    if results_number > 0: #hay que seguir scrapeando!
        next_page = driver.find_element_by_link_text("Next 100")
        next_page.click()
    #Ya levante toda la data de la pagina actual
    
    print('Cantidad de codes recolectados hasta ahora: {0}'.format(len(reference_codes)))
    print('Cantidad de subjects recolectados hasta ahora: {0}'.format(len(subjects)))
    


  


#table_results = driver.find_element_by_id("Result")
