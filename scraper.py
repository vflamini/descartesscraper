import time 
import csv
 
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager

# start by defining the options 
options = webdriver.ChromeOptions() 
options.headless = True # it's more scalable to work in headless mode 
# normally, selenium waits for all resources to download 
# we don't need it as the page also populated with the running javascript code. 
options.page_load_strategy = 'none' 
# this returns the path web driver downloaded 
chrome_path = ChromeDriverManager().install() 
chrome_service = Service(chrome_path) 
# pass the defined options and service objects to initialize the web driver 
driver = Chrome(options=options, service=chrome_service) 
driver.implicitly_wait(5)

genelist = open("genome_ensg.txt", "r")
csv_file = open("gene_list.csv", "w")
gene_val = dict()

for line in genelist:
    gene = line.lower()
    url = "https://descartes.brotmanbaty.org/bbi/human-gene-expression-during-development/gene/" + gene + "/in/placenta" 
    try:
        driver.get(url) 
        time.sleep(10)
        content = driver.find_element(By.TAG_NAME, "body").text
        number = content.split("Transcripts Per Million In Placenta:")[1].split("\n")[0].strip()
        csv_file.write("%s,%s\n" % (gene[0:len(gene)-1], number))
    except Exception as e:
        csv_file.write("%s,%s\n" % (gene, str(e)))

    