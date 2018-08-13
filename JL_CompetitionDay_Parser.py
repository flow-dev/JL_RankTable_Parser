#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
JL_CompetitionDay_Parser.py
J Data Siteから,J1,2,3の日程を取得する.
python3...
"""

__author__ = "flow_dev"

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == "__main__":

  """J1,J2,J3の日程を一括取得する"""

  url = "https://data.j-league.or.jp/SFMS01/search?competition_years=2018&tv_relay_station_name="

