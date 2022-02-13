# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 12:26:29 2022

@author: Timur Guler

Craigslist Seagull/Eastman Search Script
"""

##########
# IMPORT NECESSARY PACKAGES
##########

import pandas as pd
import numpy as np
import os
import dotenv
dotenv.load_dotenv()
import requests
import json
from bs4 import BeautifulSoup
from datetime import date, timedelta
import seagull_functions as sg

# for email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

##########
# SCRAPE CRAIGSLIST FOR SEAGULL AND EASTMAN GUITARS UNDER $1,000
##########

# user agent and urls for seagull and eastman search
headers = {'user-agent' : 'Timur Guler search for seagull guitars tguler8@gmail.com'}
seagull_url = 'https://charlottesville.craigslist.org/d/musical-instruments/search/msa?query=seagull'
eastman_url = 'https://charlottesville.craigslist.org/d/musical-instruments/search/msa?query=eastman'

# get webscraping results as bs4 objects
all_seagulls = sg.extract_html(seagull_url, headers=headers)
all_eastmans = sg.extract_html(eastman_url, headers=headers)

# get urls of individual posting pages
seagull_urls = sg.conditional_bs4_results_key(all_seagulls, 'a', 'href', 'class', 'result-image')
eastman_urls = sg.conditional_bs4_results_key(all_eastmans, 'a', 'href', 'class', 'result-image')
guitar_urls = seagull_urls + eastman_urls

# get title, price, dates, and descriptions from post
guitars = sg.get_table(guitar_urls, headers= headers)

# convert price to numeric
guitars.price = guitars.price.str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)

cutoff_date = date.today()-timedelta(days=21)
guitars = guitars[(guitars.price < 1000) & (guitars.updated >= cutoff_date)].reset_index(drop=True)

# save as csv
guitars.to_csv('..\\results\\guitars.csv', index=False)

##########
# SEND EMAIL
##########

# set up email metadata (sender/recipient, subject, etc)

sender_email = os.getenv('email_send')
receiver_email = os.getenv('email_receive')
password = os.getenv('password_dev')

message = MIMEMultipart('alternative')
message['Subject'] = f'{str(guitar_count)} New Guitars Available on Craiglist'
message['From'] = sender_email
message['To'] = receiver_email

# create email message

guitar_count = guitars.shape[0]

text = f'{guitar_count} New Guitars:\n'
for row in guitars.iterrows():
    text = text + (f'''
    {row[1].title}: ${row[1].price}
    Posted: {row[1].posted}
    Updated: {row[1].updated}
    URL: {row[1].url}
    ''')
    
# convert to MIME format and send email
mime_text = MIMEText(text, "plain")
message.attach(mime_text)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )