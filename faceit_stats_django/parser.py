import requests

print(requests.get("https://open.faceit.com/data/v4/players?nickname=TOSANDRIY",
                             headers={ "accept": "application/json", "Authorization": "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"}).text)