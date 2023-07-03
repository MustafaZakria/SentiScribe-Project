import dataset.load_restaurants as load_restaurants
import requests
import pandas as pd
import dateutil.parser
def search_dictionary(dictionary, search_name):
    for key, value in dictionary.items():
        if value['name'] == search_name:
            return key
    return None

def scrap(selected_option, number_of_reviews):

    restaurant_name = selected_option

    key = search_dictionary(load_restaurants.load_dictionary_from_file(), restaurant_name)

    if key != None:
    
        pageCtr = 1

        reviews = []
        ratings = []
        months = []
        years = []
        days = []
        
        while len(reviews) != number_of_reviews:

            try:

                url = f"https://www.elmenus.com/2.0/restaurant/{key}/review?page={pageCtr}&pageSize=20"

                payload = {}
                headers = {
                    'authority': 'www.elmenus.com',
                    'accept': 'application/json',
                    'accept-language': 'en-US,en;q=0.9',
                    'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJlbG1lbnVzLmNvbSIsInN1YiI6ImFiYjM1YzU1LWQ2ZTYtNGIwOS1iMTg0LThjMjhlMmRkMmNhMyIsImp0aSI6ImVQUkd5Z2RiYzRZdk1EWmRTcDljbnciLCJpYXQiOjE2ODYzMzQ4NjQsIm5iZiI6MTY4NjMzNDc0NCwiaXNHdWVzdCI6dHJ1ZSwiZGV2aWNlIjoiaHdvMWxpb3c4a25wIiwidmVyc2lvbiI6MS4wfQ.TdGb95gXlvBK39A3cP3CZeiNeVcEu9XKZqA9UCxQjOJuYAfbIh3dKcEkrZRkX-A6adEqnFR1_Md_mQM8BLc42g',
                    'client-model': 'WEB',
                    'client-version': '5',
                    'cookie': 'lang=EN; G_ENABLED_IDPS=google; payload=hwo1liow8knp; webRefreshToken=%242a%2412%24YtcC3TD6jOZ7u.GxtHD4C.fqJZ3WXQNhAx7v4rp%2FX6.GLmATtjpu6; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJlbG1lbnVzLmNvbSIsInN1YiI6ImFiYjM1YzU1LWQ2ZTYtNGIwOS1iMTg0LThjMjhlMmRkMmNhMyIsImp0aSI6ImVQUkd5Z2RiYzRZdk1EWmRTcDljbnciLCJpYXQiOjE2ODYzMzQ4NjQsIm5iZiI6MTY4NjMzNDc0NCwiaXNHdWVzdCI6dHJ1ZSwiZGV2aWNlIjoiaHdvMWxpb3c4a25wIiwidmVyc2lvbiI6MS4wfQ.TdGb95gXlvBK39A3cP3CZeiNeVcEu9XKZqA9UCxQjOJuYAfbIh3dKcEkrZRkX-A6adEqnFR1_Md_mQM8BLc42g; userCity=35185821-2224-11e8-924e-0242ac110011; userArea=374938a7-2224-11e8-924e-0242ac110011; userZone=0939f91e-2ee8-4b66-b772-6562bfb1ec93; _gid=GA1.2.2023646061.1686920518; X-Tracking=; _ga_SC1ZDQGQ0G=GS1.1.1686920516.10.1.1686921489.60.0.0; _ga=GA1.1.799239946.1682976402; _ga_2R1XNCQ4SC=GS1.1.1686920518.10.1.1686921489.60.0.0',
                    'device-id': 'hwo1liow8knp',
                    'device-model': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'lang': 'EN',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'userlat': '[object Object]',
                    'userlong': '[object Object]',
                    'x-client-id': '0417b144-0f3f-11e8-87cc-0242ac110002',
                    'x-device-id': 'hwo1liow8knp'
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                data = response.json()

                for i in range(20):
                    reviews.append(data['data'][i]['data']['text'])
                    ratings.append(data['data'][i]['data']['rating'])
                    date_str = data['data'][i]['trace']['created']['at']
                    date = dateutil.parser.isoparse(date_str).date()
                    days.append(date.day)
                    months.append(date.month)
                    years.append(date.year)

                pageCtr = pageCtr + 1

            except:
                break

        df = pd.DataFrame({"Reviews": reviews, 'Day': days, 'Month': months, 'Year': years})

        return None if df.empty else df
