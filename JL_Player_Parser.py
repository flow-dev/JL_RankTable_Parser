#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
JL_Player_Parser.py
J Data Siteから,選手名を取得する.
python3...
pip install zenhan
"""

__author__ = "flow_dev"

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import zenhan

if __name__ == "__main__":
    
    """BeautifulSoupでhtmlを取得する"""

    url = "https://data.j-league.or.jp/SFTD07/search?selectedCompetitionFrames=1&selectedCompetitionFrames=2&selectedCompetitionFrames=3&beginCompetitionYear=2018&endCompetitionYear=2018&totalAppearanceCount=1"
    
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    """選手に関する大枠のタグdumpを取得する"""

    PlayerDump = []

    table_tag = soup.find_all("table") #divタグを探して,選手のdumpを取る.

    for tag in table_tag:
        try:
            string_ = tag.get("class").pop(0)
            #print(string_)
            if string_ in "table-base00": #classの"pd10-box"がヘッダのdumpを引き抜く.
                PlayerDump = tag
                #print(tag)
                break
        except:
            pass
    
    """選手ごとのデータを抜き出す"""
    
    tr_tag = PlayerDump.find_all("tr") # "tr"タグで1試合ごとのデータ群が取れる.

    player_array = []
    #player_array.append(["name_", "category_", "team_", "birthdate_"])

    for tag in tr_tag:
        try:
            OnePlayerDump = tag.find_all("td") # "td"タグで1試合ごとのデータ群を意味で分けられる.
            
            # [1]:name_, ex.三浦 知良
            name_ = str(OnePlayerDump[1])
            name_ = (name_.split('-->'))[1]
            name_ = (name_.split('</td'))[0]
            name_ = zenhan.z2h(name_, mode=3)

            # [2]:name_, ex.J2
            category_ = str(OnePlayerDump[2])
            category_ = (category_.split('-->'))[1]
            category_ = (category_.split('</td'))[0]
            category_ = zenhan.z2h(category_, mode=3)

            # [4]:team_, ex.横浜FC
            team_ = OnePlayerDump[4].find("a").string
            team_ = zenhan.z2h(team_, mode=3)

            # [5]:birthdate_, ex.1967/02/26
            birthdate_ = str(OnePlayerDump[5])
            birthdate_ = (birthdate_.split('-->'))[1]
            birthdate_ = (birthdate_.split('</td'))[0]
            birthdate_ = birthdate_.strip()

            player_array.append([name_, category_, team_, birthdate_])

        except:
            pass
    
    """pandasデータフレームに変換してcsv出力する""" 
    player_dataframe = pd.DataFrame(player_array)
    player_dataframe = player_dataframe.sort_values(3) #生年月日でソート.
    player_dataframe.columns = ["name_", "category_", "team_", "birthdate_"]
    player_dataframe.to_csv('JL_2018_PlayerList_UTF8.csv' ,encoding="UTF-8" ,index=None)#, header=None)
    player_dataframe.to_csv('JL_2018_PlayerList_CP932.csv' ,index=None)#, header=None)



    