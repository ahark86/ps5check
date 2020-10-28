# ps5check

# Functionality
Scrapes nowinstock.net to confirm if Playstation 5 is in stock at any of their supported retailers. If so, sends an email to a desired address alerting the user that the item is in stock. The email links the user to noewinstock.net where the retailer-specific link can be viewed. Runs continuously scraping the site once per minute until the user interrupts it or it gets a hit on an item in stock.

# Requirements

Currently requires a Gmail account and entered Gmail credentials. Will email the user from the entered account to any recipient address of choice.
