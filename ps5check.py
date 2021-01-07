#!/usr/bin/env python

import time
import smtplib
import requests
import bs4

check_stock_url = 'https://www.nowinstock.net/videogaming/consoles/sonyps5/'
selectors = ['#tr45454 > td.stockStatus', '#tr53165 > td.stockStatus', '#tr53043 > td.stockStatus', '#tr45456 > td.stockStatus', '#tr53083 > td.stockStatus', '#tr53040 > td.stockStatus', '#tr45461 > td.stockStatus']

def send_alert(_sender_email, _recipient_email, _sender_password):
    smto_instance = smtplib.SMTP('smtp.gmail.com', 587)
    smto_instance.ehlo()
    smto_instance.starttls()
    smto_instance.login(_sender_email, _sender_password)
    smto_instance.sendmail(_sender_email, _recipient_email, 'Subject: PS5 ALERT!\nPS5 is in stock!\n {}'.format(check_stock_url))
    smto_instance.quit()

def check_stock(url):
    all_statuses = []

    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    for selector in selectors:
        vendorStatus = soup.select(selector)[0].text
        all_statuses.append(vendorStatus)

    return all_statuses

def get_senders_information():
    print('Enter your Gmail address')
    sender_email = input()

    print('Enter your Gmail password')
    sender_password = input()

    print('Enter the recipient address')
    recipient_email = input()

    return sender_email, sender_password, recipient_email

def run_scrapper():
    senders_info = get_senders_information()

    try:
        check_list = check_stock(check_stock_url)
    except IndexError:
        print('\n In stock now, check {} \n'.format(check_stock_url))
        quit()

    run_bool = True
    checks = 0

    while run_bool:
        try:
            check_list = check_stock(check_stock_url)

            for i in check_list:
                if i != "Out of Stock":
                    send_alert(*senders_info)
                    quit()

            checks += 1
            print('Out of stock. Total checks: {}'.format(checks))
            time.sleep(60)

        except IndexError:
            send_alert(*senders_info)
            print('Alert sent. Program terminating.')
            run_bool = True

    print('Program Terminated.')
    
if __name__ == "__main__":
    run_scrapper()