# RASFF-Portal-python-scraper

## Description
A Python script that extracts and analyzes the correlation between **"Substance Hazard Category"** and **"Subject"** for all product results available in the RASFF Portal from the European Commission.


## Strategy

### 1. Collect References
First, retrieve all the **reference IDs** from the result tables across all pages in the RASFF Portal (after clicking **"GET RESULTS"**):
> https://webgate.ec.europa.eu/rasff-window/portal/#

### 2. Access Detailed Records
Then, access each notification detail page by replacing the reference code in the following URL:

> https://webgate.ec.europa.eu/rasff-window/portal/?event=notificationDetail&NOTIF_REFERENCE=2020.0999
