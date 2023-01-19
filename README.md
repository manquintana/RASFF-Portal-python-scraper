RASFF-Portal-python-scraper

Description: A python script to get correlation between "Substance Hazard Category" and "Subject" for all product results given by the RASFF Portal from the European Comission

Strategy: First, I acquire all the "references" of all tables from all pages at https://webgate.ec.europa.eu/rasff-window/portal/# after pressing "GET RESULTS"
Second, I access to https://webgate.ec.europa.eu/rasff-window/portal/?event=notificationDetail&NOTIF_REFERENCE=2020.0999 changing the reference code for every single reference code (row) from the current page

Manuel Quintana 3/3/20
