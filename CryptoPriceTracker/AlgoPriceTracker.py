import time, schedule
import config

from twilio.rest import Client
from datetime import datetime
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def getTextMessage(coin, threshold, notificationType, currency = 'usd'):
  priceOfAlgo = (cg.get_price(ids=coin, vs_currencies=currency)[coin][currency])

  textMessage = None
  if priceOfAlgo <= threshold:
    textMessage = notificationType \
                + "\n" + 'Hello, the price of Algorand is ' + '$' + str(priceOfAlgo) \
                + "\n" + config.url

  return textMessage, priceOfAlgo

def sendMessage(priceMessage):
  account_sid = config.account_sid
  auth_token = config.auth_token
  client = Client(account_sid, auth_token)

  message = client.messages \
                  .create(
                      body=priceMessage,
                      from_= config.senderPhone,
                      to= config.receiverPhone
                  )

  print(message.sid)

def textLoop(threshold, notificationType):
  priceMessage, priceOfAlgo = getTextMessage('algorand', threshold, notificationType)

  now = datetime.now()
  currentTime = now.strftime("%H:%M:%S")
  if notificationType == 'ALERT:':
    print('@' + currentTime + ' Price of Algo is ' + str(priceOfAlgo))
  if priceMessage is not None:
    sendMessage(priceMessage)

def scheduleSelector(threshold, selector, notificationType, time=1):
  if selector == 'sec':
    schedule.every(time).seconds.do(textLoop, threshold, notificationType)
  elif selector == 'min':
    schedule.every(time).minutes.do(textLoop, threshold, notificationType)
  elif selector == 'hr':
    schedule.every(time).hours.do(textLoop, threshold, notificationType)

def main():
  thresholdAlert, thresholdUpdate  = 1.60, 200.00
  lengthAlert, lengthUpdate = 1, 1
  selector = ['sec', 'min', 'hr']

  scheduleSelector(thresholdAlert, selector[1], 'ALERT:', lengthAlert)
  scheduleSelector(thresholdUpdate, selector[2], 'UPDATE:', lengthUpdate)

  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
  main()