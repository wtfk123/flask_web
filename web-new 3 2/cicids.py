from pymongo import MongoClient
import base64
import requests
from bson import binary
from flask_paginate import get_page_parameter, Pagination
import json
import subprocess
import os
import sys
# import chardet
from datetime import datetime,timedelta
# import Response
import pandas as pd


client=MongoClient('mongodb://localhost:27017')
db1=client['net_army']

date_fields = {
    '推特推文': 'tweetDate',  # 替换为实际字段名
    '微博数据': 'created_at',  # 替换为实际字段名
    '媒体网站新闻数据': 'date',  # 替换为实际字段名
    'ins推文': 'pubDate',  # 替换为实际字段名
    '微博数据': '发布时间',  # 替换为实际字段名
}


def get_data():
    start_date = datetime(2024, 7, 30)
    end_date = datetime(2024, 9, 30)
    
    # 存储每天的数据总量
    daily_totals = {}

    # 统计每个集合的数据
    for collection_name, date_field in date_fields.items():
        collection = db1[collection_name]
        for single_date in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
            date_str = single_date.strftime('%Y-%m-%d')
            # 匹配年月日
            # start_of_day = single_date.replace(hour=0, minute=0, second=0, microsecond=0)
            # end_of_day = single_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            # count = collection.count_documents({
            #     date_field: {
            #         '$gte': start_of_day,
            #         '$lte': end_of_day  # 统计当天的数据
            #     }
            # })
            # daily_totals[single_date.strftime('%Y-%m-%d')] = daily_totals.get(single_date.strftime('%Y-%m-%d'), 0) + count
            count = collection.count_documents({
                date_field: date_str  # 直接匹配字符串
            })

            daily_totals[date_str] = daily_totals.get(date_str, 0) + count

    print(daily_totals)

get_data()