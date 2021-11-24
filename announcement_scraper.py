#!/bin/python3
import requests
import os
import json
import smtplib
import ssl
import time
from random import randint
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

def send_notification(announcement):
    """
    Uses SMTP to send an email which contains the announcement
    """

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sent_from = os.getenv("EMAIL")
    to = os.getenv("EMAIL")
    subject = announcement
    body = 'Read more at https://www.binance.com/en/support/announcement/c-48'
    message = f'Subject: {subject}\n\n{body}'

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sent_from, os.getenv("PASSWORD"))
            server.sendmail(sent_from, to, message)

    except Exception as e:
        print(e)


def store_announcement(file, announcement):
    """
    Save announcement into local json file
    """
    with open(file, "w") as f:
        json.dump(announcement, f, indent=4)
        
        
def load_json(file):
    """
    Update Json file
    """
    with open(file, "r+") as f:
        return json.load(f)


# terms to exclude
EXCLUSIONS = ['Futures', 'Margin', 'adds']

def get_last_announcement():
    """
    Scraps the last binance announcement
    """
    try:
        page = requests.get("https://www.binance.com/en/support/announcement/c-48")

        if str(page.status_code)[0] == "2":
            
            soup = BeautifulSoup(page.content, "lxml")
            
            title = soup.find(id="link-0-0-p1").text
            
            for word in EXCLUSIONS:
                if word in title:
                    return None
            
            return title
        
    except Exception as e:
        print(e)


def is_new(announcement):
    """
    Returns True if it is and stores it in announcement.json
    """
    
    if os.path.isfile("announcement.json"):

        file = load_json("announcement.json")
        
        if announcement in file:
            return False
        
        store_announcement("announcement.json", announcement)        
        return True
    
    new_listing = store_announcement('announcement.json', announcement)
    return True


def main(seconds):
    """
    Scraps Binance and send an email if it finds a new announcement
    """
    while True:
        announcement = get_last_announcement()
        
        if announcement:
            if is_new(announcement):
                send_notification(announcement)

        time.sleep(seconds)


if __name__ == "__main__":
    main(randint(5, 10))