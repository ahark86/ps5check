#!/usr/bin/env python

import time, smtplib, requests, bs4

selectors = ['#tr45454 > td.stockStatus', '#tr53165 > td.stockStatus', '#tr53043 > td.stockStatus', '#tr45456 > td.stockStatus', '#tr53083 > td.stockStatus', '#tr53040 > td.stockStatus', '#tr45461 > td.stockStatus']
allStatuses = []
checks = 0
stop = 0

def sendAlert(fromAddress, recipient, password):
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(f'{fromAddress}', f'{password}')
	smtpObj.sendmail(f'{fromAddress}', f'{recipient}', 'Subject: PS5 ALERT!\nPS5 is in stock!\nhttps://www.nowinstock.net/videogaming/consoles/sonyps5/')
	smtpObj.quit()

def checkStock(url):
	res = requests.get(url)
	res.raise_for_status()

	soup = bs4.BeautifulSoup(res.text, 'html.parser')

	for s in selectors:
		vendorStatus = soup.select(f'{s}')[0].text
		allStatuses.append(vendorStatus)

	return allStatuses

print('Enter your Gmail address')
fromAdd = input()

print('Enter your Gmail password')
passw = input()

print('Enter the recipient address')
recip = input()

try:
	checkList = checkStock('https://www.nowinstock.net/videogaming/consoles/sonyps5/')
except IndexError:
	print('\n' + 'In stock now, check https://www.nowinstock.net/videogaming/consoles/sonyps5/' + '\n')
	quit()

while stop == 0:
	try:
		checkList = checkStock('https://www.nowinstock.net/videogaming/consoles/sonyps5/')
		
		for i in checkList:
			if i != "Out of Stock":
				sendAlert(fromAdd, recip, passw)
				quit()

		checks += 1
		print(f'Out of stock. Total checks: {checks}')
		time.sleep(60)
	except IndexError:
		sendAlert(fromAdd, recip, passw)
		print('Alert sent. Program terminating.')
		stop = 1

print('Program Terminated.')