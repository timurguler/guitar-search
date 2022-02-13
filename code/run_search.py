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
import requests
import json
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import seagull_functions as sg

# for email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


##########
# SCRAPE CRAIGSLIST FOR SEAGULL AND EASTMAN GUITARS UNDER $1,000
##########

# user agent, urls, and search terms for seagull and eastman search

path = os.getcwd()
os.chdir('..')
dotenv.load_dotenv()
os.chdir(path)

headers = {'user-agent' : 'Timur Guler search for seagull guitars tguler8@gmail.com'}
clist_url = os.getenv('url')
terms = os.getenv('terms').split(',')

# build search urls
search_urls = [clist_url + '/msa?query=' + term for term in terms]

# get webscraping results as bs4 objects
search_results = [sg.extract_html(url, headers=headers) for url in search_urls]

# get urls of individual posting pages
page_urls = []
for result in search_results:
    page_urls = page_urls + sg.conditional_bs4_results_key(result, 'a', 'href', 'class', 'result-image')

# get title, price, dates, and descriptions from post
guitars = sg.get_table(page_urls, headers= headers)

# convert price to numeric
guitars.price = guitars.price.str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)

# define cutoff date based on range from .env file and filter
search_range = int(os.getenv('range'))
cutoff_date = datetime.combine(date.today()-timedelta(days=search_range), datetime.min.time())
guitars = guitars[(guitars.price < 1000) & (guitars.updated >= cutoff_date)].reset_index(drop=True)

# bring in previous results and compare to current
prev_results = pd.read_csv('..\\results\\guitars.csv')
prev_results.posted = pd.to_datetime(prev_results.posted)
prev_results.updated = pd.to_datetime(prev_results.updated)

new_guitars, seen_guitars = sg.compare_with_previous(guitars, prev_results)

# save list of all guitars seen up to this point
seen_guitars.to_csv('..\\results\\guitars.csv', index=False)

##########
# SEND EMAIL
##########

guitar_count = new_guitars.shape[0]

if guitar_count > 0:
    # set up email metadata (sender/recipient, subject, etc)

    sender_email = os.getenv('email_send')
    receiver_email = os.getenv('email_receive')
    password = os.getenv('password_dev')

    message = MIMEMultipart('alternative')
    message['Subject'] = f'{str(guitar_count)} New Guitar(s) Available on Craiglist'
    message['From'] = sender_email
    message['To'] = receiver_email

    # create email message

    text = f'{guitar_count} New Guitar(s):\n'
    for row in new_guitars.iterrows():
        text = text + (f'''
        {row[1].title}: ${row[1].price}
        Posted: {row[1].posted.date()}
        Updated: {row[1].updated.date()}
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