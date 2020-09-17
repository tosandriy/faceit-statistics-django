import requests

print(requests.get(
        "https://open.faceit.com/data/v4/matches/1-93e16a1d-b096-4aef-b223-4cadc6143e29/stats",
        headers={"accept" : "application/json",
                 "Authorization" : "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"}).text)