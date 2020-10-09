import time
import urllib
import requests
 
client_id = '6PML9SNDDS4UV2SRA5ASTV5BBKF6DSX9'

endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format('IBM')

# define the payload
payload = {'apikey':client_id,
           'periodType':'day',
           'frequencyType':'minute',
           'frequency':'1'}

# make a request
content = requests.get(url = endpoint, params = payload)

# convert it dictionary object
data = content.json()

print(data)