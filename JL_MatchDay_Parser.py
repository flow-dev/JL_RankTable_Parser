#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
JL_MatchDay_Parser.py
J Data Siteから,J1,2,3の日程を取得する.
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

    url = "https://data.j-league.or.jp/SFMS01/search?competition_years=2018&tv_relay_station_name="
    
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify(formatter="html")) #文字化けするので,htmlで確認.


    """日程に関する大枠のタグdumpを取得する"""

    CompetitionDayDump = []

    div_tag = soup.find_all("div") #divタグを探して,日程のdumpを取る.

    for tag in div_tag:
        try:
            string_ = tag.get("class").pop(0)
            #print(string_)
            if string_ in "pd10-box": #classの"pd10-box"がヘッダのdumpを引き抜く.
                CompetitionDayDump = tag
                #print(tag)
                break
        except:
            pass
    #print(CompetitionDayDump.prettify(formatter="html")) #文字化けするので,htmlで確認.


    """1試合ごとのデータを抜き出す"""
    
    tr_tag = CompetitionDayDump.find_all("tr") # "tr"タグで1試合ごとのデータ群が取れる.

    # 1試合ごとのデータをリスト化する配列を用意する.
    competition_array = []
    competition_array.append(["year_", "category_", "section_", "date_", "time_", "hometeam_", "score_", "awayteam_", "stadium_", "visitors_", "broadcast_"]) #ヘッダー.

    for tag in tr_tag:
        try:
            OneMatchDump = tag.find_all("td") # "td"タグで1試合ごとのデータ群を意味で分けられる.

            #[0]:year_, ex.2018
            year_       = OneMatchDump[0].string
            
            #[1]:category_, ex.J1
            category_   = OneMatchDump[1].string
            category_   = zenhan.z2h(category_, mode=3) #mode=3は英数のみ半角.
    
            #[2]:section_, ex.第1節第1日
            if(str(OneMatchDump[2].string) == "None"): #空文字の場合があるので場合分け.
                section_  = "None"
            else:
                section_    = OneMatchDump[2].string
                section_    = zenhan.z2h(section_, mode=3) #mode=3は英数のみ全角->半角変換.    
            
            #[3]:date_, ex.02/23(金)
            date_       = OneMatchDump[3].string

            #[4]:time_, ex.20:03
            time_       = OneMatchDump[4].string
            time_       = time_.strip() #TAB文字と改行コードを消す.

            #[5]:hometeam_, ex.鳥栖
            hometeam_   = OneMatchDump[5].find("a").string #tagの中から"a"タグの中身を取得.
            hometeam_   = zenhan.z2h(hometeam_, mode=3) #mode=3は英数のみ全角->半角変換. 

            #[6]:score_, ex.1-1
            if(str(OneMatchDump[6].string) == "None"): #空文字の場合があるので場合分け.
                score_      = OneMatchDump[6].find("a").string #tagの中から"a"タグの中身を取得. 
            else:
                score_      = "None"

            #[7]:awayteam_, ex.神戸
            awayteam_   = OneMatchDump[7].find("a").string #tagの中から"a"タグの中身を取得.
            awayteam_   = zenhan.z2h(awayteam_, mode=3) #mode=3は英数のみ全角->半角変換. 

            #[8]:stadium_, ex.ベアスタ
            stadium_    = OneMatchDump[8].string
            stadium_    = stadium_.strip() #TAB文字と改行コードを消す.
            stadium_    = zenhan.z2h(stadium_, mode=3) #mode=3は英数のみ全角->半角変換. 

            #[9]:visitors_, ex.19,633    
            visitors_   = OneMatchDump[9].string
            visitors_   = visitors_.strip() #TAB文字と改行コードを消す.
            if(str(visitors_)==""): #html構造がここだけ異なるので,空文字の扱いが別.
                visitors_ = "None"

            #[9]:broadcast_, ex.DAZN
            if(str(OneMatchDump[10].string) == "None"):
                broadcast_  = "None"
            else:
                broadcast_  = OneMatchDump[10].string
                broadcast_  = broadcast_.strip() #TAB文字と改行コードを消す.
                broadcast_  = zenhan.z2h(broadcast_, mode=3) #mode=3は英数のみ全角->半角変換. 
            
            #配列に1試合毎のデータを代入する.
            competition_array.append([year_, category_, section_, date_, time_, hometeam_, score_, awayteam_, stadium_, visitors_, broadcast_])
            
        except:
            pass


        """pandasデータフレームに変換してcsv出力する"""        
        
        competition_dataframe = pd.DataFrame(competition_array)
        competition_dataframe.to_csv('JL_MatchDay_UTF8.csv' ,encoding="UTF-8" ,index=None, header=None)
        competition_dataframe.to_csv('JL_MatchDay_CP932.csv' ,index=None, header=None)
        
        