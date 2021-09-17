import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
from lookups import countries
from parse_player_data import induv_stats


def get_players(country: str):
    players = {}
    current_player_list_url = 'https://www.espncricinfo.com/player/team/'
    url = current_player_list_url + country + '-' + str(countries[country])
    print(country, url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    p = soup.find_all('div', class_='index-data p-3')
    for ele in p:
        try:
            pid = re.findall(r'\d+', ele.find('a')['href'])[0]
            pname = ele.find('p').getText()
            players[pname] = int(pid)
        except:
            print('Error generating name or id of player with info: ', pname)
    return players


def get_player_stats_dfs(country: str, players: dict, pid=0, wtf=False):
    players = get_players(country)
    if pid > 0:
        players = {k: v for k, v in players.items() if players[k] == pid}
        print(players)
    else:
        pass
    for player in players.keys():
        pid = players[player]
        player_url = ("https://stats.espncricinfo.com/ci/engine/player/{}.html?class=11;"
                      "template=results;type=allround;view=match".format(pid))
        df = pd.read_html(player_url)
        induv_stat = induv_stats(df)
        if wtf:
            file = "..\\Data\\Cricketers\\{}\\{}.csv".format(country, player)
            os.makedirs("..\\Data\\Cricketers\\{}".format(country), exist_ok=True)
            induv_stat.to_csv(file, index=False)
        else:
            return induv_stat


if __name__ == '__main__':
    get_player_stats_dfs('england', players=get_players('england'), pid=8917, wtf=False)
