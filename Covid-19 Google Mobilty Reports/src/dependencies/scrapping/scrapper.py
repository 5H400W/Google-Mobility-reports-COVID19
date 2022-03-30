# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 14:28:17 2022

@author: Prashant Dwivedi


"""


#importing Libraries

from pandas import DataFrame, to_datetime
from datetime import datetime
import os
import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging
import time

try:
    from tika import parser 
    # pip install tika
except:
    #%pip install tika
    from tika import parser


class parse_data:
    def __init__(self, url= "https://www.google.com/covid19/mobility/"):
        self.url = url
        self.data= DataFrame()
        self.pdf_url = []
        self.field_to_be_extract = []
        logging.info("data initialized")        
        print("data initialized")

        
    def dump_pdfs_in_local(self): 
        folder_location = "pdfs"
        cwd_= os.getcwd()
        if not os.path.exists(os.path.join(cwd_,folder_location)):os.mkdir(os.path.join(cwd_,folder_location))
        for pdf in self.pdf_url[:50]:
            filename = pdf.split("/")[-1] 
            filename = os.path.join(cwd_,folder_location,filename)
            with open(filename, 'wb') as f:
                f.write(requests.get(pdf).content)
            logging.info("...")
        logging.info("data dump to local")
        print("data dump to local")

                
    
             
    def filter_todays_url(self):
        pdf_url = []
        for file in self.pdf_url:
            filename = file.split("/")[-1] 
            if datetime.now().date()==to_datetime(filename.split('_')[0]).date():
                pdf_url.append(file)
        self.pdf_url = pdf_url
        return self.pdf_url
    
    
    def filter_english_content(self):
        pdf_url = []
        for file in self.pdf_url:
            filename = file.split("/")[-1] 
            if  filename[-6:] == "en.pdf":
                pdf_url.append(file)
        self.pdf_url = pdf_url
        logging.info("content filterd for english language")
        print("content filterd for english language")

        
        
        
        
    def get_pdf_url(self):
        
        response = requests.get(self.url)
        soupe= BeautifulSoup(response.text, "html.parser")    
        soupes = soupe.find_all(text=re.compile("www.gstatic.com"))
        data=(str(soupes[0])+str(soupes[1])).replace("\\","")
        self.pdf_url = re.findall("https://www.gstatic.com/covid19/mobility/[^x]*pdf",data)
        #self.pdf_url = self.filter_todays_url() #uncomment only when todays data is available with todays it self date
        logging.info("PDF URLS are fetched")
        print("PDF URLS are fetched")

        
    @staticmethod
    def add_data(raw,key):
        try:
            idx=raw.index(key)
            if raw[idx+1][1:-1].isnumeric():
                return raw[idx+1][:-1]
            return ""
        except Exception as e:
            return ""
            
    
    def get_pdf_data(self):
        data={"country_region_code":[],
              "country_region":[],
              "_region_1":[],
              "_region_2":[],
              "metro_area"	:[],
              "iso_3166_2_code":[],	
              "census_fips_code":[],	
              "place_id":[],
              "date":[],	
              "retail_and_recreation_percent_change_from_baseline":[],	
              "grocery_and_pharmacy_percent_change_from_baseline":[],	
              "parks_percent_change_from_baseline":[],
              "transit_stations_percent_change_from_baseline":[],
              "workplaces_percent_change_from_baseline"	:[],
              "residential_percent_change_from_baseline":[]
        }

        folder_location = "//pdfs"
        cwd_=os.getcwd()
        files=os.listdir("\pdfs")
        for file in files:
            try:
                raw = parser.from_file(os.path.join((str(os.getcwd())+"\pdfs\\" + file)))
                date = file.split("_")[0]
                code=file.split("_")[1]
                raw=raw["content"].split("\n")
                raw_new=[]
                for i in raw:
                    if i!="":
                        raw_new.append(i)
                country= " ".join(raw_new[1].split(" ")[:-3])
                data["date"].append(date)
                data["country_region_code"].append(code)
                data["country_region"].append(country)
                data["retail_and_recreation_percent_change_from_baseline"].append(self.add_data(raw_new,"Retail & recreation"))
                data["grocery_and_pharmacy_percent_change_from_baseline"].append(self.add_data(raw_new,"Grocery & pharmacy"))
                data["parks_percent_change_from_baseline"].append(self.add_data(raw_new,"Parks"))
                data["transit_stations_percent_change_from_baseline"].append(self.add_data(raw_new,"Transit stations"))
                data["workplaces_percent_change_from_baseline"].append(self.add_data(raw_new,"Workplaces"))
                data["residential_percent_change_from_baseline"].append(self.add_data(raw_new,"Residential"))
                data["_region_1"].append(self.add_data(raw_new,"_region_1"))
                data["_region_2"].append(self.add_data(raw_new,"_region_2"))
                data["metro_area"].append(self.add_data(raw_new,"metro_area"))
                data["iso_3166_2_code"].append(self.add_data(raw_new,"metro_area"))
                data["census_fips_code"].append(self.add_data(raw_new,"census_fips_code"))
                data["place_id"].append(self.add_data(raw_new,"place_id"))
            except Exception as e:
                continue
        logging.info("successfully extract the data")
        print("successfully extract the data")

        return DataFrame(data)
    
   

while True:
    my_scraper= parse_data()
    my_scraper.get_pdf_url()
    my_scraper.filter_english_content()
    my_scraper.dump_pdfs_in_local()
    data=my_scraper.get_pdf_data()
    data.to_excel(str(datetime.datetime.now().date())+"_"+str(len(os.listdir(os.getcwd()))+1)+"_"+"google_mobility_data.xlsx")
    logging.info("file saved")
    print("process done")
    print("Next run will be after 24 hours")
    time.sleep(60 * 60 * 24)
    

            
 