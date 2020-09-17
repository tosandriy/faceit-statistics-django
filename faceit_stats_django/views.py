from django.shortcuts import render,redirect
import requests
import json
from datetime import datetime



def index_view(request):
    if request.GET:
        try:
            username = request.GET["search_field"]
            return redirect("statistics",user_name=username)
        except:
            pass
    return render(request,"first_page.html", {})


def statistic_view(request, user_name):
    user_info = requests.get("https://open.faceit.com/data/v4/players?nickname=Enotik1338",
                             headers={ "accept": "application/json", "Authorization": "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"}).text
    user_info = json.loads(user_info)

    return render(request,"test.html", {"faceit_username": user_info["nickname"],
                                         "user_picture": user_info["avatar"],
                                         "country": user_info["country"],
                                         "last_infraction_date":user_info["infractions"]["last_infraction_date"],
                                         "afk": user_info["infractions"]["afk"],
                                         "leaver": user_info["infractions"]["leaver"],
                                         "platforms": user_info["platforms"],
                                         "last_games": user_info["games"],
                                         "language": user_info["settings"]["language"],
                                         "friends_id_list": user_info["friends_ids"]
                                         })


def statistics_view(request, user_name):
    user_info = requests.get("https://open.faceit.com/data/v4/players?nickname=Enotik1338",
                             headers={ "accept": "application/json", "Authorization": "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"}).text

    last_games = requests.get("https://open.faceit.com/data/v4/players/bad4f87f-b5fb-45da-9d57-f7cd8b9540ba/history?game=csgo&offset=0&limit=20",
                             headers={"accept" : "application/json",
                                      "Authorization" : "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"}).text

    user_stat = requests.get(
        "https://open.faceit.com/data/v4/players/bad4f87f-b5fb-45da-9d57-f7cd8b9540ba/stats/csgo",
        headers={"accept" : "application/json",
                 "Authorization" : "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"}).text

    user_info = json.loads(user_info)
    last_games = json.loads(last_games)
    user_stat = json.loads(user_stat)
    match_id_list = []

    for game in last_games["items"]:
        match_id_list.append(game["match_id"])

    player_maps = []
    for match_id in match_id_list:
        match_stat = requests.get(
                f"https://open.faceit.com/data/v4/matches/{match_id}/stats",
                headers={"accept" : "application/json",
                         "Authorization" : "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"}).text
        match_stat_main = json.loads(match_stat)
        match_stat = match_stat_main["rounds"][0]["teams"][0]["players"]
        team_name1 = match_stat_main["rounds"][0]["teams"][0]["team_stats"]["Team"]
        team_name2 = match_stat_main["rounds"][0]["teams"][1]["team_stats"]["Team"]
        players_list1 = []
        for player in match_stat:
            players_list1.append((player["nickname"],player["player_stats"]["Kills"],
                                 player["player_stats"]["Assists"], player["player_stats"]["Deaths"],
                                 player["player_stats"]["K/R Ratio"],
                                 round(int(player["player_stats"]["Kills"]) / int(player["player_stats"]["Deaths"]),2),

                                 player["player_stats"]["Headshot"],player["player_stats"]["Headshots %"],
                                  player["player_stats"]["MVPs"],
                                 player["player_stats"]["Triple Kills"], player["player_stats"]["Quadro Kills"],
                                 player["player_stats"]["Penta Kills"],player["player_stats"]["Result"]))
        players_list1.sort(key=lambda x: int(x[1]))
        players_list1.reverse()
        match_stat = match_stat_main["rounds"][0]["teams"][1]["players"]
        players_list2 = []
        for player in match_stat :
            players_list2.append((player["nickname"], player["player_stats"]["Kills"],
                                 player["player_stats"]["Assists"],
                                 player["player_stats"]["Deaths"],
                                 player["player_stats"]["K/R Ratio"],
                                 round(int(player["player_stats"]["Kills"])/int(player["player_stats"]["Deaths"]),2),
                                 player["player_stats"]["Headshot"],player["player_stats"]["Headshots %"],
                                 player["player_stats"]["MVPs"], player["player_stats"]["Triple Kills"],
                                 player["player_stats"]["Quadro Kills"],
                                 player["player_stats"]["Penta Kills"], player["player_stats"]["Result"]))
        players_list2.sort(key=lambda x: int(x[1]))
        players_list2.reverse()
        if players_list1[0][-1] == '1':
            player_maps.append((players_list1,players_list2,team_name1,team_name2))
        else:
            player_maps.append((players_list2, players_list1,team_name2,team_name1))



    match_stat = requests.get(
        f"https://api.faceit.com/stats/api/v1/stats/time/users/bad4f87f-b5fb-45da-9d57-f7cd8b9540ba/games/csgo").text
    match_stat = json.loads(match_stat)
    maps_info_list = []
    for xx in range(20) :
        x_last = match_stat[xx + 1]
        x = match_stat[xx]
        maps_info_list.append((True if x["i10"] == "1" else False, x["i18"], x["i5"], x["i6"], x["i7"], x["i8"], x["c2"], x["c3"],
              round(int(x["i13"]) / int(x["i6"]), 2) // 0.01, x["elo"], int(x["elo"]) - int(x_last["elo"]),
              datetime.utcfromtimestamp(int(x["updated_at"]) / 1000).strftime('%Y-%m-%d %H:%M'), x["i1"],player_maps[xx]))
    for x in maps_info_list:
        print(x)

    last_games_win_rate = int(match_stat[0]["i10"])
    last_games_hs_rate = int(match_stat[0]["c4"])
    last_games_avg_kills = int(match_stat[0]["i6"])
    try:
        last_games_kd = int(match_stat[0]["i6"]) / int(match_stat[0]["i8"]) or 1
        empty = False
    except IndexError:
        last_games_kd = 0
        empty = True
    if not empty:
        for game in match_stat[1:20]:
            last_games_avg_kills += int(game["i6"])
            last_games_kd = int(game["i6"]) / int(game["i8"] or 1) + last_games_kd
            last_games_hs_rate += int(game["c4"])
            last_games_win_rate += int(game["i10"])

        last_games_kd /= 20
        last_games_win_rate = (last_games_win_rate / 20) * 100
        last_games_hs_rate /= 20
        last_games_avg_kills /= 20

    return render(request,"stats.html", {"faceit_username": user_info["nickname"],
                                         "user_picture": user_info["avatar"],
                                         "country": user_info["country"],
                                         "last-infraction-date":user_info["infractions"]["last_infraction_date"],
                                         "afk": user_info["infractions"]["afk"],
                                         "leaver": user_info["infractions"]["leaver"],
                                         "platforms": user_info["platforms"],
                                         "last-games": user_info["games"],
                                         "language": user_info["settings"]["language"],
                                         "friends-id-list": user_info["friends_ids"],

                                         "k_d": user_stat["lifetime"]["Average K/D Ratio"],
                                         "win_rate": user_stat["lifetime"]["Win Rate %"],
                                         "hs_rate": user_stat["lifetime"]["Average Headshots %"],
                                         "total_matches":user_stat["lifetime"]["Matches"],
                                         "longest_win_streak": user_stat["lifetime"]["Longest Win Streak"],
                                         "last_games_results": user_stat["lifetime"]["Recent Results"],
                                         "k_d_ratio":user_stat["lifetime"]["K/D Ratio"],
                                         "cur_ws": user_stat["lifetime"]["Current Win Streak"],
                                         "total_wins":user_stat["lifetime"]["Wins"],

                                         "last_games_kd": round(last_games_kd,2),
                                         "last_games_win_rate": round(last_games_win_rate),
                                         "last_games_hs_rate": round(last_games_hs_rate),
                                         "last_games_avg_kills": round(last_games_avg_kills,2),

                                         "maps_info_list": maps_info_list,
                                         })