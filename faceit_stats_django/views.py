from django.shortcuts import render, redirect
import requests
import json
from datetime import datetime
import threading
import time


def index_view(request) :
    if request.GET :
        try :
            username = request.GET["search_field"]
            return redirect("statistics", user_name=username)
        except :
            pass
    return render(request, "first_page.html", {})


def statistics_view(request, user_name) :
    start_time = time.time()
    player_maps = []

    def get_user_info() :
        user_info = requests.get(
                f"https://open.faceit.com/data/v4/players?nickname={user_name}",
                headers={"accept" : "application/json",
                         "Authorization" : "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"
                         }).text

        user_info = json.loads(user_info)

        return user_info

    def get_last_games(player_id) :
        last_games = requests.get(
                f"https://open.faceit.com/data/v4/players/{player_id}/history?game=csgo&offset=0&limit=20",
                headers={"accept" : "application/json",
                         "Authorization" : "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"
                         }).text

        last_games = json.loads(last_games)
        return last_games

    def get_user_stat(player_id) :
        user_stat = requests.get(
                f"https://open.faceit.com/data/v4/players/{player_id}/stats/csgo",
                headers={"accept" : "application/json",
                         "Authorization" : "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"
                         }).text

        user_stat = json.loads(user_stat)
        return user_stat

    def get_match_stat(player_id,quantity):
        match_stat = requests.get(
                f"https://api.faceit.com/stats/api/v1/stats/time/users/{player_id}/games/csgo").text
        match_stat = json.loads(match_stat)
        match_list = []
        last_match_num = -1
        for i in range(quantity+1):
            while 1:
                last_match_num += 1
                if match_stat[last_match_num]["gameMode"] == "5v5" \
                    and "elo" in match_stat[last_match_num] \
                    and not match_stat[last_match_num]["i1"].startswith("workshop/"):
                    match_list.append(match_stat[last_match_num])
                    break
        return match_list

    def match_info_worker(match_id,counter) :
        match_stat = requests.get(
                f"https://open.faceit.com/data/v4/matches/{match_id}/stats",
                headers={"accept" : "application/json",
                         "Authorization" : "Bearer 07975108-f7ed-46dd-9e58-962350c09afd"}).text
        match_stat_main = json.loads(match_stat)
        match_stat1 = match_stat_main["rounds"][0]["teams"][0]["players"]
        team_name1 = match_stat_main["rounds"][0]["teams"][0]["team_stats"]["Team"]
        team_name2 = match_stat_main["rounds"][0]["teams"][1]["team_stats"]["Team"]
        players_list1 = []
        for player in match_stat1 :
            players_list1.append((player["nickname"], player["player_stats"]["Kills"],
                                  player["player_stats"]["Assists"], player["player_stats"]["Deaths"],
                                  player["player_stats"]["K/R Ratio"],
                                  round(int(player["player_stats"]["Kills"]) / int(player["player_stats"]["Deaths"]),
                                        2),

                                  player["player_stats"]["Headshot"], player["player_stats"]["Headshots %"],
                                  player["player_stats"]["MVPs"],
                                  player["player_stats"]["Triple Kills"], player["player_stats"]["Quadro Kills"],
                                  player["player_stats"]["Penta Kills"], player["player_stats"]["Result"]))
        players_list1.sort(key=lambda x : int(x[1]))
        players_list1.reverse()
        match_stat2 = match_stat_main["rounds"][0]["teams"][1]["players"]
        players_list2 = []
        for player in match_stat2 :
            players_list2.append((player["nickname"], player["player_stats"]["Kills"],
                                  player["player_stats"]["Assists"],
                                  player["player_stats"]["Deaths"],
                                  player["player_stats"]["K/R Ratio"],
                                  round(int(player["player_stats"]["Kills"]) / int(player["player_stats"]["Deaths"]),
                                        2),
                                  player["player_stats"]["Headshot"], player["player_stats"]["Headshots %"],
                                  player["player_stats"]["MVPs"], player["player_stats"]["Triple Kills"],
                                  player["player_stats"]["Quadro Kills"],
                                  player["player_stats"]["Penta Kills"], player["player_stats"]["Result"]))
        players_list2.sort(key=lambda x : int(x[1]))
        players_list2.reverse()
        if players_list1[0][-1] == '1' :
            player_maps.append((players_list1, players_list2, team_name1, team_name2,counter))
        else :
            player_maps.append((players_list2, players_list1, team_name2, team_name1,counter))

    user_info = get_user_info()
    try:
        player_id = user_info["player_id"]
    except KeyError:
        return redirect('index')

    last_games = get_last_games(player_id)
    user_stat = get_user_stat(player_id)

    match_id_list = []
    for game in last_games["items"] :
        match_id_list.append(game["match_id"])
    match_stat = get_match_stat(player_id, 20)
    for x in range(20) :
        t = threading.Thread(target=match_info_worker, args=(match_stat[x]["matchId"],x))
        t.start()

    maps_info_list = []
    elo_list = []
    while 1 :
        if len(player_maps) == 20 :
            print(player_maps)
            player_maps = sorted(player_maps,key= lambda k: k[4])
            break
        time.sleep(0.01)

    for xx in range(20) :
        x = match_stat[xx]
        x_last = match_stat[xx + 1]

        elo_list.append(x["elo"])
        maps_info_list.append((True if x["i10"] == "1" else False, x["i18"], x["i5"], x["i6"], x["i7"], x["i8"],
                               x["c2"], x["c3"], round(int(x["i13"]) / int(x["i6"]), 2) // 0.01, x["elo"],
                               int(x["elo"]) - int(x_last["elo"]),
                               datetime.utcfromtimestamp(int(x["updated_at"]) / 1000).strftime('%Y-%m-%d %H:%M'),
                               x["i1"], player_maps[xx]))
    elo_list.reverse()
    last_games_win_rate = int(match_stat[0]["i10"])
    last_games_hs_rate = int(match_stat[0]["c4"])
    last_games_avg_kills =int(match_stat[0]["i6"])
    try :
        last_games_kd = int(match_stat[0]["i6"]) / int(match_stat[0]["i8"]) or 1
        empty = False
    except IndexError :
        last_games_kd = 0
        empty = True
    if not empty :
        for game in match_stat[1 :20] :
            last_games_avg_kills += int(game["i6"])
            last_games_kd = int(game["i6"]) / int(game["i8"] or 1) + last_games_kd
            last_games_hs_rate += int(game["c4"])
            last_games_win_rate += int(game["i10"])

        last_games_kd /= 20
        last_games_win_rate = (last_games_win_rate / 20) * 100
        last_games_hs_rate /= 20
        last_games_avg_kills /= 20
    print(time.time() - start_time)
    return render(request, "stats.html", {"faceit_username" : user_info["nickname"],
                                          "user_picture" : user_info["avatar"],
                                          "country" : user_info["country"],
                                          "last-infraction-date" : user_info["infractions"]["last_infraction_date"],
                                          "afk" : user_info["infractions"]["afk"],
                                          "leaver" : user_info["infractions"]["leaver"],
                                          "platforms" : user_info["platforms"],
                                          "steam_id_64" : user_info["steam_id_64"],
                                          "faceit_url" : user_info["faceit_url"].replace("{lang}", "en"),
                                          "last-games" : user_info["games"],
                                          "language" : user_info["settings"]["language"],
                                          "friends-id-list" : user_info["friends_ids"],
                                          "elo_list" : (int(x) for x in elo_list),
                                          "elo" : match_stat[0]["elo"],

                                          "k_d" : user_stat["lifetime"]["Average K/D Ratio"],
                                          "win_rate" : user_stat["lifetime"]["Win Rate %"],
                                          "hs_rate" : user_stat["lifetime"]["Average Headshots %"],
                                          "total_matches" : user_stat["lifetime"]["Matches"],
                                          "longest_win_streak" : user_stat["lifetime"]["Longest Win Streak"],
                                          "last_games_results" : user_stat["lifetime"]["Recent Results"],
                                          "k_d_ratio" : user_stat["lifetime"]["K/D Ratio"],
                                          "cur_ws" : user_stat["lifetime"]["Current Win Streak"],
                                          "total_wins" : user_stat["lifetime"]["Wins"],

                                          "last_games_kd" : round(last_games_kd, 2),
                                          "last_games_win_rate" : round(last_games_win_rate),
                                          "last_games_hs_rate" : round(last_games_hs_rate),
                                          "last_games_avg_kills" :  f"{round(last_games_avg_kills, 2):.2f}",

                                          "maps_info_list" : maps_info_list,
                                          })
