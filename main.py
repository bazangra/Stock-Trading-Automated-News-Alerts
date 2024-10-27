from twilio.rest import Client
from datetime import datetime, timedelta
import requests

stock_api = "VC3V8VQSX60JH1EN"
news_api = "2c2b680a73d64bbf8f1fde7256b538b6"

account_sid = 'ACbbb8fba945900aa7f2a1f4116d1b4ab3'
auth_token = '3a82e7c3b683c8f2d3bd6f80ad1cc50c'
api_key = "ba745ec27bb5d154e7ca2bb08e2bc42c"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

today = str(datetime.now()).split()[0]
yesterday = (str(datetime.now() - timedelta(1))).split()[0]
day_before_yesterday = str((datetime.now() - timedelta(2))).split()[0]

stock_para = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api,
}

response = requests.get(url="https://www.alphavantage.co/query", params=stock_para)
response.raise_for_status()
data = response.json()
print(data)

price_diff = int(2)
# (float(data["Time Series (Daily)"][yesterday]["4. close"])/float(data["Time Series (Daily)"][day_before_yesterday]["4. close"])-1)*100)
print(price_diff)

if 5 <= price_diff or -5 >= price_diff:
    print("get news")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

news_para = {"qInTitle": "Tesla", "from": yesterday, "sortBy": "popularity", "apiKey": news_api}
response = requests.get("https://newsapi.org/v2/everything", params=news_para)
data = response.json()["articles"]
print(data[:3])

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

if price_diff >= 0:
    send = f"TSLA: 🔺{abs(price_diff)}%\nHeadline: {data[0]["title"]}\nBrief: {data[0]["description"]}"
else:
    send = f"TSLA: 🔻{abs(price_diff)}%\nHeadline: {data[0]["title"]}\nBrief: {data[0]["description"]}"

client = Client(account_sid, auth_token)
message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=send,
    to='whatsapp:+447711259832'
)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

