from django.shortcuts import render,redirect
import requests

def index_view(request):
    return render(request,"first_page.html", {})


def statistic_view(request, user_name):
    user_stat = requests.get("https://open.faceit.com/data/v4/players?nickname=TOSANDRIY",
                             headers={ "accept": "application/json", "Authorization": "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"}).text

    return render(request,"stats.html", {"faceit_username": user_stat["nickname"],
                                         "game_username": user_stat["game_player_name"],
                                         "steam_username": user_stat["steam_nickname"],
                                         "user_picture": user_stat["avatar"],
                                         "country": user_stat["country"],
                                         "last_infraction_date":user_stat["infraction"]["last_infraction_date"],
                                         "afk": user_stat["infraction"]["afk"],
                                         "leaver": user_stat["infraction"]["leaver"],
                                         "platforms": user_stat["platforms"],
                                         "last_games": user_stat["games"],
                                         "language": user_stat["settings"]["language"],
                                         "friends_id_list": user_stat["friends_ids"]
                                         })
