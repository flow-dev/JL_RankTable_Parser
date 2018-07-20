#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
JL_RankTable_Parser.py
J Data Siteから,J1,2,3の順位表を取得する.
python3...
"""

__author__ = "flow_dev"

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

class JdateSite_RankParse(object):
    """ Jの最新順位データをパースする. """
    def __init__(self,soup):
        self.modified_date  = "None" #更新日時.
        self.modified_time  = "None" #更新時間.
        self.rank_num       = 1      #順位はカウンタで.
        self.team_name      = "None" #チーム名.
        self.team_logo      = "None" #チームロゴのリンク.
        self.soup           = soup
    
    def GetDateModified(self,):
        """ 順位が更新された日時を取得する. """
        date_tag = self.soup.find_all("p") #pタグで更新時間取得可能なhtml構造である.
    
        for tag in date_tag:
            try:
                string_ = tag
                self.modified_date = tag.string.split()[0]
                self.modified_time = tag.string.split()[1] 
                break
            except:
                pass
        return
    
    def GetRankDump(self,):
        """順位に関するHtmlDumpを取得する."""
        div_tag = self.soup.find_all("div") #divタグでHtmlDump取得可能なhtml構造である.
        RankBoxDump = "None"
        for tag in div_tag:
            try:
                string_ = tag.get("class").pop(0)
                if string_ in "tab-rank-box":
                    RankBoxDump = tag
                    #print(self.RankBoxDmup)
                    break
            except:
                pass
        return (RankBoxDump)
    
    def ParseRankBoxDmup(self, RankBoxDump):
        """順位に関するHtmlDumpから必要なデータを抜き出す"""
        img = RankBoxDump.find_all("img") #imgタグでHtmlDump取得可能なhtml構造である.
        rank_array = []
        rank_array.append(["UpdateDate", "UpdateTime", "Rank", "TeamName", "TeamLogo"]) #ヘッダー.
    
        for tag in img:
            try:
                self.team_name = tag.get("alt")
                self.team_logo = "https://data.j-league.or.jp" + tag.get("src") #https://...追加.
                rank_array.append([self.modified_date, self.modified_time, self.rank_num, self.team_name, self.team_logo])
                self.rank_num = self.rank_num + 1
            except:
                pass
        
        #pandasデータフレームに変換.
        rank_array = pd.DataFrame(rank_array)

        return (rank_array)


def GetLeageRankToDataFrame(url):
    """Jの最新順位データ取得し,PandasDataFrameで返す."""
    
    # URLにアクセスとhtmlが帰ってくる.
    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う.
    soup = BeautifulSoup(html, "html.parser")

    # Jの最新順位データをパースする.
    J_DATE_RANK = JdateSite_RankParse(soup)
    J_DATE_RANK.GetDateModified()
    RankBoxDump = J_DATE_RANK.GetRankDump()
    rank_dataframe = J_DATE_RANK.ParseRankBoxDmup(RankBoxDump)

    return (rank_dataframe)


if __name__ == "__main__":
    
    """J1,J2,J3の順位,チーム名,チームロゴを一括取得する"""

    # アクセスするURL
    url_J1 = "https://data.j-league.or.jp/SFTP01/?startPage=0&endPage=5&competitionFrameId=1&prev_next=&nextBtnVal=0&prevBtnVal=0"
    url_J2 = "https://data.j-league.or.jp/SFTP01/?startPage=0&endPage=5&competitionFrameId=2&prev_next=&nextBtnVal=0&prevBtnVal=0"
    url_J3 = "https://data.j-league.or.jp/SFTP01/?startPage=0&endPage=5&competitionFrameId=3&prev_next=&nextBtnVal=0&prevBtnVal=0"

    # Jの最新順位データ取得し,PandasDataFrameで返す.
    rank_dataframe_J1 = GetLeageRankToDataFrame(url_J1)
    rank_dataframe_J2 = GetLeageRankToDataFrame(url_J2)
    rank_dataframe_J3 = GetLeageRankToDataFrame(url_J3)

    # パースしたデータをcsvで保存する.
    rank_dataframe_J1.to_csv('J1_RankTable_UTF8.csv' ,encoding="UTF-8" ,index=None, header=None)
    rank_dataframe_J2.to_csv('J2_RankTable_UTF8.csv' ,encoding="UTF-8" ,index=None, header=None)
    rank_dataframe_J3.to_csv('J3_RankTable_UTF8.csv' ,encoding="UTF-8" ,index=None, header=None)
