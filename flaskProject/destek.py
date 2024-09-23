

import requests
def dolarkuru():
    # API'den döviz kuru verisini çek
    url = 'https://v6.exchangerate-api.com/v6/39d220b73c477c3ace1b3f79/latest/USD'
    usd = requests.get(url).json()
    birdolar= usd.get("conversion_rates").get("TRY")
    return birdolar

