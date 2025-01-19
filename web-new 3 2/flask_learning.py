from flask import Flask
from flask import render_template,send_from_directory,send_file
from flask import request, redirect,url_for,jsonify
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
from bson import ObjectId
import gridfs
from io import BytesIO
import random

app = Flask(__name__)
app.static_folder = 'static'

client=MongoClient('mongodb://localhost:27017')

db1=client['net_army']
collection1=db1['媒体网站军事数据']
collection2=db1['媒体网站新闻数据']
collection3 = db1['推特推文']
collection4=db1['推特重点人物粉丝']
collection5=db1['ins推文']
collection6=db1['微博数据']
collection7=db1['世界主要媒体']
collection8=db1['全球智库 ']
collection9=db1['活跃且有影响力的账户']
collection10=db1['政府官方媒体']
collection11=db1['重要人物(港澳台)']
collection12=db1['重要人物(海外)']
collection13=db1['推特重点名人网红']
collection15=db1['脸书重点名人网红']
collection16=db1['重要社交媒体']
collection17=db1['军事网站']
collection18=db1['ins重点名人网红']
collection19=db1['国家情况描述']
collection20=db1['国家机构构成']
collection21=db1['民间社会（部落）组织']
collection22=db1['各国从属党派']
collection23=db1['宗教基本信息']
collection24=db1['各国宗教信仰']
collection25=db1['政党政策及影响信息']
collection26=db1['经济势力信息']
collection27=db1['历史沿革数据']
collection28=db1['对于事件各国的立场']
collection29=db1['国际事件与冲突']
collection30=db1['各国贸易关系']
collection31=db1['国际关系']
collection32=db1['地缘政治地理信息数据']
collection33=db1['国际政治（军事、经济）组织功能描述']
collection34=db1['媒体网站说明']
collection35=db1['多模态数据']
collection36=db1['人物、组织、媒体（外部数据）']
fs = gridfs.GridFS(db1)

date_fields = {
    '推特推文': 'tweetDate',  # 替换为实际字段名
    '媒体网站新闻数据': 'date',  # 替换为实际字段名
    'ins推文': 'pubDate',  # 替换为实际字段名
    '微博数据': '发布时间',  # 替换为实际字段名
    '推特重点人物粉丝': 'date',  # 替换为实际字段名
    '媒体网站军事数据': 'date',  # 替换为实际字段名
    '脸书重点名人网红': 'timestamp',  # 替换为实际字段名
    '推特重点名人网红': 'timestamp',  # 替换为实际字段名
    'ins重点名人网红': 'timestamp',  # 替换为实际字段名
    '全球智库': 'timestamp',  # 替换为实际字段名
    '人物、组织、媒体（外部数据）': '发表时间',  # 替换为实际字段名
}



##################################################################################mult
@app.route('/data_mult/date_show',methods=['GET',"POST"])
def get_data_mult1():
        # 获取分页参数
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get('date')
    query = {"tweetDate": {'$regex': selected_date_str, '$options': 'i'}}
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    data35 = collection35.find(query).skip(skip=skip).limit(per_page).sort("tweetDate", -1)
    total = collection35.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    # 从 MongoDB 获取数据
    

    return render_template('mult_data.html', data35=data35, selected_date= selected_date_str,pagination=pagination)

@app.route('/data_mult/show',methods=['GET'])
def get_data_mult2():
        # 获取分页参数
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data35 = collection35.find().skip(skip=skip).limit(per_page).sort("tweetDate", -1)
    total = collection35.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    

    return render_template('mult_data.html', data35=data35,pagination=pagination)
@app.route('/data_mult/search_show',methods=['GET',"POST"])
def get_data_mult3():
        # 获取分页参数
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    keyword = request.args.get('keyword')
    query ={
        "$or": [
            {'tweetContent':{'$regex': keyword, '$options': 'i'}},
            {'handle':{'$regex': keyword, '$options': 'i'}},
            {'query':{'$regex': keyword, '$options': 'i'}}
            ]
        }
    data35 = collection35.find(query).skip(skip=skip).limit(per_page).sort("tweetDate", -1)
    total = collection35.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    # 从 MongoDB 获取数据


    return render_template('mult_data.html', data35=list(data35),search_data= keyword,pagination=pagination)
# ############################################################################echarts
@app.route('/charts_show', methods=['GET'])
def pie_nest_data():

    collections = db1.list_collection_names()
    collection_data = []
    total_count = 0
    filtered_count = 0  # 只累加符合条件的文档数量

    # 获取今天的日期
    today = datetime.now().strftime('%Y-%m-%d')  # 格式化为 YYYY-MM-DD

    for collection in collections:
        # 获取每个集合的总文档数量
        count = db1[collection].count_documents({})
        collection_data.append({'name': collection, 'count': count})
        total_count += count  # 累加总文档数量
    print(total_count)

    # 计算2024年的数据量
    for collection_name, date_field in date_fields.items():
        collection = db1[collection_name]
        
        # 计算符合日期条件的文档数量
        year_count = collection.count_documents({
            date_field: {
                '$gte': "2023-09-30",  # 设定开始日期
                '$lt': "2024-09-30"     # 设定结束日期
            }
        })
        filtered_count += year_count  # 累加符合条件的文档数量
    print(filtered_count)
    # 计算占比
    proportion = round((filtered_count / total_count * 100), 3) if total_count > 0 else 0

    collection_count = len(collections)

    return render_template('charts_show.html', 
                           collection_data=collection_data, 
                           total_count=total_count, 
                           collection_count=collection_count, 
                           proportion=proportion)

########################################################################################图像展示
@app.route('/data', methods=['GET',"POST"])
def get_data():
    start_date = datetime(2024, 7, 30)
    end_date = datetime(2024, 9, 30)
    
    # 存储每天的数据总量
    daily_totals = {}

    # 统计每个集合的数据
    for collection_name, date_field in date_fields.items():
        collection = db1[collection_name]
        for single_date in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
            # 匹配年月日
            #并需要将匹配的数据变为字符串类型
            date_str = single_date.strftime('%Y-%m-%d')
            count = collection.count_documents({
                date_field: date_str  # 直接匹配字符串
            })

            daily_totals[date_str] = daily_totals.get(date_str, 0) + count
    return jsonify(daily_totals)

############################################################################1
#军事数据日期数据查询
@app.route('/data1/date_search', methods=['get','POST'])
def date1_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get('date')
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"date":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection1.find(query).skip(skip=skip).limit(per_page).sort("date", -1)
    total = collection1.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('net_army_data.html',data1=matched_events, pagination=pagination, selected_date= selected_date_str)
# @app.route('/search', methods=['POST'])
# def search():
#     # 获取表单中输入的Twitter链接
#     twitter_link = request.form['twitter_link']

#     # 在MongoDB中执行查询
#     query = { "tweetLink": twitter_link }
#     video_data = collection20.find_one(query)

#     if video_data:
#         video_url = video_data["videoUrl"]
#         return render_template('video.html', video_url=video_url)
#     else:
#         return "Video URL not found for the given Twitter link.
#data1，军事数据搜索功能
@app.route('/search/data1', methods=['GET', 'POST'])
def data_search1():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {
        "$or": [
            {'name':{'$regex': keyword, '$options': 'i'}},
            {'information':{'$regex': keyword, '$options': 'i'}},
            {'editor':{'$regex': keyword, '$options': 'i'}}
            ]
        }
    # 根据关键字查询数据
    data_search1 = collection1.find(query).skip(skip=skip).limit(per_page).sort("date", -1)
    total = collection1.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('net_army_data.html', data1=list(data_search1), search_data=keyword,pagination=pagination)
#data1军事数据展示
@app.route("/show/data1",methods=["GET", "POST"])
def info():
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data1 = collection1.find().skip(skip=skip).limit(per_page).sort("date", -1)
    data1 = list(data1)
    total = collection1.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('net_army_data.html', data1=data1,pagination=pagination)
    
    
###################################################################################2
    
    
#data2新闻数据展示
@app.route("/show/data2",methods=["GET", "POST"])
def render1():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data2 = collection2.find().skip(skip=skip).limit(per_page).sort("date", -1)
    total = collection2.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('net_news_data.html', data2=data2,pagination=pagination)
#data2,新闻数据时间查询
@app.route('/data2/date_search', methods=['get','POST'])
def date2_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get('date')
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"date":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection2.find(query).skip(skip=skip).limit(per_page).sort("date", -1)
    total = collection2.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('net_news_data.html',data2=matched_events, pagination=pagination, selected_date=selected_date_str)

#data2,新闻数据搜索功能
@app.route('/search/data2', methods=['GET', 'POST'])
def data_search2():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {"$or":
        [{'name':{'$regex': keyword, '$options': 'i'}},
        {'editor':{'$regex': keyword, '$options': 'i'}},
        {'information':{'$regex': keyword, '$options': 'i'}}
                ]
            }
    # 根据关键字查询数据
    data_search2 = collection2.find(query).skip(skip=skip).limit(per_page).sort("date", -1)
    total = collection2.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('net_news_data.html', data2=data_search2,pagination=pagination,search_data=keyword)

################################################################################3
#data3数据,tweet搜索功能
@app.route('/search/data3', methods=['GET', 'POST'])
def data_search3():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'twitterId':{'$regex': keyword, '$options': 'i'}},
            {'handle':{'$regex': keyword, '$options': 'i'}},
            {'text':{'$regex': keyword, '$options': 'i'}},
            {'type':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search3 = collection3.find(query).skip(skip=skip).limit(per_page).sort("tweetDate", -1)
    total = collection3.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('twitter_tuiwen.html', data3=list(data_search3),pagination=pagination,search_data=keyword)

@app.route("/show/data3",methods=["GET", "POST"])
def render2():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data3 = collection3.find().skip(skip=skip).limit(per_page).sort("tweetDate", -1)
    total = collection3.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('twitter_tuiwen.html',data3=data3,pagination=pagination)

@app.route('/data3/date_search', methods=['GET','POST'])
def date3_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.form['date']
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"tweetDate":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection3.find(query).skip(skip=skip).limit(per_page).sort("tweetDate", -1)
    total = collection3.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('twitter_tuiwen.html',data3=matched_events, pagination=pagination,selected_date=selected_date_str)

#########################################################################################4
#data4数据,推特重点人物粉丝搜索功能
@app.route('/search/data4', methods=['GET', 'POST'])
def data_search4():
    keyword = request.args.get('keyword')
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'screenName':{'$regex': keyword, '$options': 'i'}},
            {'name':{'$regex': keyword, '$options': 'i'}},
            {'bio':{'$regex': keyword, '$options': 'i'}},
            {'location':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search4 = collection4.find(query).skip(skip=skip).limit(per_page).sort("createdAt", -1)
    total = collection4.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('twitter_follower.html', data4=list(data_search4),pagination=pagination,search_data=keyword)
#推特重点人物粉丝展示功能
@app.route("/show/data4",methods=["GET", "POST"])
def render3():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data4 = collection4.find().skip(skip=skip).limit(per_page).sort("createdAt", -1)
    total = collection4.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('twitter_follower.html', data4=data4,pagination=pagination)
@app.route('/data4/date_search', methods=['get','POST'])
def date4_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get['date']
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"date":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection4.find(query).skip(skip=skip).limit(per_page).sort("createdAt", -1)
    total = collection4.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('twitter_follower.html',data4=matched_events, pagination=pagination,selected_date=selected_date_str)

###########################################################################################5
#data5数据,ins推文搜索功能
@app.route('/search/data5', methods=['GET', 'POST'])
def data_search5():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'description':{'$regex': keyword, '$options': 'i'}},
            {'location':{'$regex': keyword, '$options': 'i'}},
            {'type':{'$regex': keyword, '$options': 'i'}},
            {'caption':{'$regex': keyword, '$options': 'i'}},
            {'username':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search5 = collection5.find(query).skip(skip=skip).limit(per_page).sort("pubDate", -1)
    total = collection5.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('ins_tuiwen.html', data5=list(data_search5),pagination=pagination, search_data=keyword)
@app.route("/show/data5",methods=["GET", "POST"])
def render4():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data5 = collection5.find().skip(skip=skip).limit(per_page).sort("pubDate", -1)
    total = collection5.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('ins_tuiwen.html', data5=data5,pagination=pagination)

@app.route('/data5/date_search', methods=['GET','POST'])
def date5_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get['date']
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"pubDate":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection5.find(query).skip(skip=skip).limit(per_page).sort("pubDate", -1)
    total = collection5.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('ins_tuiwen.html',data5=matched_events, pagination=pagination,selected_date=selected_date_str)

###############################################################################################6
#data6数据,微博数据搜索功能
@app.route('/search/data6', methods=['GET', 'POST'])
def data_search6():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'screen_name':{'$regex': keyword, '$options': 'i'}},
            {'text':{'$regex': keyword, '$options': 'i'}},
            {'source':{'$regex': keyword, '$options': 'i'}},
            {'ip':{'$regex': keyword, '$options': 'i'}},
            {'user_authentication':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search6 = collection6.find(query).skip(skip=skip).limit(per_page).sort("发布时间", -1)
    total = collection6.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('weibo_data.html', data6=list(data_search6),search_data=keyword,pagination=pagination)

@app.route("/show/data6",methods=["GET", "POST"])
def render5():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data6 = collection6.find().skip(skip=skip).limit(per_page).sort("发布时间", -1)

    total = collection6.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('weibo_data.html', data6=data6,pagination=pagination)

@app.route('/data6/date_search', methods=['GET','POST'])
def date6_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get['date']
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"created_at":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection6.find(query).skip(skip=skip).limit(per_page).sort("发布时间", -1)
    total = collection6.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('weibo_data.html',data6=matched_events,selected_date=selected_date_str,pagination=pagination)

#################################################################################################7
#data7数据,世界主要媒体搜索功能
@app.route('/search/data7', methods=['GET', 'POST'])
def data_search7():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'C1组织基本信息':{'$regex': keyword, '$options': 'i'}},
            {'C6组织简介':{'$regex': keyword, '$options': 'i'}},
            {'C3组织重点人物':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search7 = collection7.find(query).skip(skip=skip).limit(per_page)
    total = collection7.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('main_world_net.html', data7=list(data_search7),pagination=pagination,search_data=keyword)

@app.route("/show/data7",methods=["GET", "POST"])
def render7():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data6 = collection7.find().skip(skip=skip).limit(per_page)
    total = collection7.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('main_world_net.html', data7=data6,pagination=pagination)

# @app.route('/data7/date_search', methods=['POST'])
# def date6_search():
#     page = request.args.get(get_page_parameter(), type=int, default=1)

#     # 每页显示的数据量
#     per_page = 10
#     skip = (page - 1) * per_page
#     selected_date_str = request.form['date']
#     # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
#     query = {"created_at":{'$regex': selected_date_str, '$options': 'i'}}
#     matched_events = collection7.find(query).skip(skip=skip).limit(per_page)
#     total = collection7.count_documents(query)
#     # 分页处理
#     pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
#     return render_template('weibo_data.html',data6=matched_events, pagination=pagination)
#################################################################################################8
#data8数据,全球智库搜索功能
@app.route('/search/data8', methods=['GET', 'POST'])
def data_search8():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'tt_name_en':{'$regex': keyword, '$options': 'i'}},
            {'strapline':{'$regex': keyword, '$options': 'i'}},
            {'description':{'$regex': keyword, '$options': 'i'}},
            {'main_city':{'$regex': keyword, '$options': 'i'}},
            {'country':{'$regex': keyword, '$options': 'i'}},
            {'address':{'$regex': keyword, '$options': 'i'}},
            {'g_email':{'$regex': keyword, '$options': 'i'}},
            {'operating_langs':{'$regex': keyword, '$options': 'i'}},
            {'web_events':{'$regex': keyword, '$options': 'i'}},
            {'tt_business_model':{'$regex': keyword, '$options': 'i'}},
            {'tt_affiliations':{'$regex': keyword, '$options': 'i'}},
            {'topics':{'$regex': keyword, '$options': 'i'}},
            {'geographies':{'$regex': keyword, '$options': 'i'}},
            {'founder':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search8 = collection8.find(query).skip(skip=skip).limit(per_page).sort("date_founded", -1)
    total = collection8.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('world_base.html', data8=list(data_search8),pagination=pagination,search_data=keyword)

@app.route("/show/data8",methods=["GET", "POST"])
def render8():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data8 = collection8.find().skip(skip=skip).limit(per_page).sort("date_founded", -1)
    data8 = list(data8)
    total = collection8.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('world_base.html',data8=data8,pagination=pagination)

@app.route('/data8/date_search', methods=['GET','POST'])
def date8_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get['date']
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"date_founded":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection8.find(query).skip(skip=skip).limit(per_page).sort("date_founded", -1)
    total = collection8.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('world_base.html',data8=matched_events, pagination=pagination,selected_date=selected_date_str)
#####################################################################################################9
#data9数据,活跃且具有影响力的账户搜索功能
@app.route('/search/data9', methods=['GET', 'POST'])
def data_search9():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'机构':{'$regex': keyword, '$options': 'i'}},
            {'screenName':{'$regex': keyword, '$options': 'i'}},
            {'name':{'$regex': keyword, '$options': 'i'}},
            {'location':{'$regex': keyword, '$options': 'i'}},
            {'certified':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search9 = collection9.find(query).skip(skip=skip).limit(per_page).sort("createdAt", -1)
    total = collection9.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('Active_account.html', data9=list(data_search9),pagination=pagination,search_data=keyword)

@app.route("/show/data9",methods=["GET", "POST"])
def render9():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data9 = collection9.find().skip(skip=skip).limit(per_page).sort("createdAt", -1)
    total = collection9.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('Active_account.html',data9=data9,pagination=pagination)

@app.route('/data9/date_search', methods=['get','POST'])
def date9_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get['date']
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"createdAt":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection9.find(query).skip(skip=skip).limit(per_page).sort("createdAt", -1)
    total = collection9.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('Active_account.html',data9=matched_events, pagination=pagination,selected_date=selected_date_str)
#########################################################################################################10
#data10数据,政府官方媒体搜索功能
@app.route('/search/data10', methods=['GET', 'POST'])
def data_search10():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'网站名称':{'$regex': keyword, '$options': 'i'}},
            {'url':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search10 = collection10.find(query).skip(skip=skip).limit(per_page)
    total = collection10.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('Official.html', data10=list(data_search10),pagination=pagination,search_data=keyword)

@app.route("/show/data10",methods=["GET", "POST"])
def render10():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data10 = collection10.find().skip(skip=skip).limit(per_page)
    total = collection10.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('Official.html',data10=data10,pagination=pagination)
#########################################################################################################11
#data11数据,重点人物(港澳台)搜索功能
@app.route('/search/data11', methods=['GET', 'POST'])
def data_search11():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'类目B':{'$regex': keyword, '$options': 'i'}},
            {'人名':{'$regex': keyword, '$options': 'i'}},
            {'译名':{'$regex': keyword, '$options': 'i'}},
            {'政治倾向':{'$regex': keyword, '$options': 'i'}},
            {'组织机构':{'$regex': keyword, '$options': 'i'}},
            {'职务':{'$regex': keyword, '$options': 'i'}},
            {'经历':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search11 = collection11.find(query).skip(skip=skip).limit(per_page)
    total = collection11.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('important_people_gat.html', data11=list(data_search11),pagination=pagination,search_data=keyword)

@app.route("/show/data11",methods=["GET", "POST"])
def render11():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data11 = collection11.find().skip(skip=skip).limit(per_page)
    total = collection11.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('important_people_gat.html',data11=data11,pagination=pagination)
#########################################################################################################12
#data12数据,重点人物(海外)搜索功能
@app.route('/search/data12', methods=['GET', 'POST'])
def data_search12():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'美国':{'$regex': keyword, '$options': 'i'}},
            {'国会议员':{'$regex': keyword, '$options': 'i'}},
            {'人名':{'$regex': keyword, '$options': 'i'}},
            {'译名':{'$regex': keyword, '$options': 'i'}},
            {'党派':{'$regex': keyword, '$options': 'i'}},
            {'党派职务':{'$regex': keyword, '$options': 'i'}},
            {'政治倾向':{'$regex': keyword, '$options': 'i'}},
            {'组织机构':{'$regex': keyword, '$options': 'i'}},
            {'职务工作':{'$regex': keyword, '$options': 'i'}},
            {'简历经历':{'$regex': keyword, '$options': 'i'}},
        ]
        }
    # 根据关键字查询数据
    data_search12 = collection12.find(query).skip(skip=skip).limit(per_page)
    total = collection12.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('important_people_out.html', data12=list(data_search12),pagination=pagination,search_data=keyword)

@app.route("/show/data12",methods=["GET", "POST"])
def render12():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data12 = collection12.find().skip(skip=skip).limit(per_page)
    total = collection12.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('important_people_out.html',data12=data12,pagination=pagination)
#########################################################################################################13
#推特重点名人网红
#data13数据
@app.route('/search/data13', methods=['GET', 'POST'])
def data_search13():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'handle':{'$regex': keyword, '$options': 'i'}},
            {'location':{'$regex': keyword, '$options': 'i'}},
            {'name':{'$regex': keyword, '$options': 'i'}},
            {'verified':{'$regex': keyword, '$options': 'i'}},
        ]
        }
    # 根据关键字查询数据
    data_search13 = collection13.find(query).skip(skip=skip).limit(per_page).sort("joinDate", -1)
    total = collection13.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('V_twitter.html', data13=list(data_search13),pagination=pagination,search_data=keyword)

@app.route("/show/data13",methods=["GET", "POST"])
def render13():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data13 = collection13.find().skip(skip=skip).limit(per_page).sort("joinDate", -1)
    total = collection13.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('V_twitter.html',data13=data13,pagination=pagination)

@app.route('/data13/date_search', methods=['get','POST'])
def date13_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get['date']
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"joinDate":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection13.find(query).skip(skip=skip).limit(per_page).sort("joinDate", -1)
    total = collection13.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('V_twitter.html',data13=matched_events, pagination=pagination,selected_date=selected_date_str)
#########################################################################################################15
#脸书重点名人网红
#data15数据
@app.route('/search/data15', methods=['GET', 'POST'])
def data_search15():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'fullName':{'$regex': keyword, '$options': 'i'}},
            {'workName':{'$regex': keyword, '$options': 'i'}},
            {'educationName':{'$regex': keyword, '$options': 'i'}},
            {'workDescription':{'$regex': keyword, '$options': 'i'}},
            {'educationDescription':{'$regex': keyword, '$options': 'i'}},
            {'locationName':{'$regex': keyword, '$options': 'i'}},
            {'locationType':{'$regex': keyword, '$options': 'i'}},
            {'relationship':{'$regex': keyword, '$options': 'i'}},
            {'bio':{'$regex': keyword, '$options': 'i'}},
        ]
        }
    # 根据关键字查询数据
    data_search15 = collection15.find(query).skip(skip=skip).limit(per_page).sort("timestamp", -1)
    total = collection15.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('V_facebook.html', data15=list(data_search15),pagination=pagination,search_data=keyword)

@app.route("/show/data15",methods=["GET", "POST"])
def render15():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data15 = collection15.find().skip(skip=skip).limit(per_page).sort("timestamp", -1)
    total = collection15.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('V_facebook.html',data15=data15,pagination=pagination)

@app.route('/data15/date_search', methods=['get','POST'])
def date15_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get['date']
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"timestamp":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection15.find(query).skip(skip=skip).limit(per_page).sort("timestamp", -1)
    total = collection15.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('V_facebook.html',data15=matched_events, pagination=pagination,selected_date=selected_date_str)


#########################################################################################################16
#data16数据,重要社交媒体搜索功能
@app.route('/search/data16', methods=['GET', 'POST'])
def data_search16():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'媒体网站':{'$regex': keyword, '$options': 'i'}},
            {'微博':{'$regex': keyword, '$options': 'i'}},
            {'facebook':{'$regex': keyword, '$options': 'i'}},
            {'twitter':{'$regex': keyword, '$options': 'i'}},
            {'instgram':{'$regex': keyword, '$options': 'i'}},
            {'LinkedIn':{'$regex': keyword, '$options': 'i'}},
            {'政府机构':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search7 = collection16.find(query).skip(skip=skip).limit(per_page).sort("timestamp", -1)
    total = collection16.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('important_social.html', data16=list(data_search7),pagination=pagination,search_data=keyword)

@app.route("/show/data16",methods=["GET", "POST"])
def render16():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data17 = collection16.find().skip(skip=skip).limit(per_page).sort("timestamp", -1)
    total = collection16.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('important_social.html', data16=data17,pagination=pagination)


@app.route('/data16/date_search', methods=['get','POST'])
def date16_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get['date']
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"timestamp":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection16.find(query).skip(skip=skip).limit(per_page).sort("timestamp", -1)
    total = collection16.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('important_social.html',data16=matched_events, pagination=pagination,selected_date=selected_date_str)
#########################################################################################################17
#data17数据,美国企业及军事媒体搜索功能
@app.route('/search/data17', methods=['GET', 'POST'])
def data_search17():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'网站名':{'$regex': keyword, '$options': 'i'}},
            {'url':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search7 = collection17.find(query).skip(skip=skip).limit(per_page)
    total = collection17.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('army_net.html', data17=list(data_search7),pagination=pagination,search_data=keyword)

@app.route("/show/data17",methods=["GET", "POST"])
def render17():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data17 = collection17.find().skip(skip=skip).limit(per_page)
    total = collection17.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('army_net.html', data17=data17,pagination=pagination)

###############################################################################################################18
#data18数据,ins重点人物搜索功能
@app.route('/search/data18', methods=['GET', 'POST'])
def data_search18():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'username':{'$regex': keyword, '$options': 'i'}},
            {'isVerified':{'$regex': keyword, '$options': 'i'}},
            {'id':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search7 = collection18.find(query).skip(skip=skip).limit(per_page)
    total = collection18.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('V_ins.html', data18=list(data_search7),pagination=pagination,search_data=keyword)

@app.route("/show/data18",methods=["GET", "POST"])
def render18():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data17 = collection18.find().skip(skip=skip).limit(per_page)
    total = collection18.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('V_ins.html', data18=data17,pagination=pagination)
###############################################################################################################19
#data19数据,国家情况描述数据搜索功能
@app.route('/search/data19', methods=['GET', 'POST'])
def data_search19():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'数字代码':{'$regex': keyword, '$options': 'i'}},
            {'中文名称':{'$regex': keyword, '$options': 'i'}},
            {'英文名称':{'$regex': keyword, '$options': 'i'}},
            {'国家或地区':{'$regex': keyword, '$options': 'i'}},
            {'所在洲':{'$regex': keyword, '$options': 'i'}},
            {'所在地区':{'$regex': keyword, '$options': 'i'}},
            {'电话区号':{'$regex': keyword, '$options': 'i'}},
            {'域名':{'$regex': keyword, '$options': 'i'}},
            {'英文缩写':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search7 = collection19.find(query).skip(skip=skip).limit(per_page)
    total = collection19.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('country_introduction.html', data19=list(data_search7),pagination=pagination,search_data=keyword)

@app.route("/show/data19",methods=["GET", "POST"])
def render19():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data17 = collection19.find().skip(skip=skip).limit(per_page)
    total = collection19.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('country_introduction.html', data19=data17,pagination=pagination)
###############################################################################################################20
#data20数据,国家机构构成搜索功能
@app.route('/search/data20', methods=['GET', 'POST'])
def data_search20():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'编号':{'$regex': keyword, '$options': 'i'}},
            {'国家':{'$regex': keyword, '$options': 'i'}},
            {'机构构成':{'$regex': keyword, '$options': 'i'}},
            {'描述':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search20 = collection20.find(query).skip(skip=skip).limit(per_page)
    total = collection20.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('State_institution.html', data20=list(data_search20),pagination=pagination,search_data=keyword)

@app.route("/show/data20",methods=["GET", "POST"])
def render20():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data20 = collection20.find().skip(skip=skip).limit(per_page)
    total = collection20.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('State_institution.html', data20=data20,pagination=pagination)
###############################################################################################################21
#data21数据,民间社会(部落)组织搜索功能
@app.route('/search/data21', methods=['GET', 'POST'])
def data_search21():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'编号':{'$regex': keyword, '$options': 'i'}},
            {'国家':{'$regex': keyword, '$options': 'i'}},
            {'民间社会组织或部落':{'$regex': keyword, '$options': 'i'}},
            {'社会结构':{'$regex': keyword, '$options': 'i'}},
            {'领导人物':{'$regex': keyword, '$options': 'i'}},
            {'相关介绍':{'$regex': keyword, '$options': 'i'}},
            {'主要活动':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search21 = collection21.find(query).skip(skip=skip).limit(per_page)
    total = collection21.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('governmental_organization.html', data21=list(data_search21),pagination=pagination,search_data=keyword)

@app.route("/show/data21",methods=["GET", "POST"])
def render21():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data21 = collection21.find().skip(skip=skip).limit(per_page)
    total = collection21.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('governmental_organization.html', data21=data21,pagination=pagination)
###############################################################################################################22
#data22数据,各国从属党派搜索功能
@app.route('/search/data22', methods=['GET', 'POST'])
def data_search22():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'编号':{'$regex': keyword, '$options': 'i'}},
            {'从属党派及国家':{'$regex': keyword, '$options': 'i'}},
            {'英文名称':{'$regex': keyword, '$options': 'i'}},
            {'成立时间':{'$regex': keyword, '$options': 'i'}},
            {'党最高领导人/书记主席':{'$regex': keyword, '$options': 'i'}},
            {'副主席/书记':{'$regex': keyword, '$options': 'i'}},
            {'党内分支及各负责人':{'$regex': keyword, '$options': 'i'}},
            {'相关描述':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search22 = collection22.find(query).skip(skip=skip).limit(per_page)
    total = collection22.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('National_party.html', data22=list(data_search22),pagination=pagination,search_data=keyword)

@app.route("/show/data22",methods=["GET", "POST"])
def render22():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data22 = collection22.find().skip(skip=skip).limit(per_page)
    total = collection22.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('National_party.html', data22=data22,pagination=pagination)
###############################################################################################################23
#data23数据,宗教基本信息搜索功能
@app.route('/search/data23', methods=['GET', 'POST'])
def data_search23():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'编号':{'$regex': keyword, '$options': 'i'}},
            {'宗教':{'$regex': keyword, '$options': 'i'}},
            {'宗教_en':{'$regex': keyword, '$options': 'i'}},
            {'创始人':{'$regex': keyword, '$options': 'i'}},
            {'现任领导人':{'$regex': keyword, '$options': 'i'}},
            {'成立时间':{'$regex': keyword, '$options': 'i'}},
            {'描述（包括主要信仰，历史起源、分布范围等）':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search23 = collection23.find(query).skip(skip=skip).limit(per_page)
    total = collection23.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('religion_basic.html', data23=list(data_search23),pagination=pagination,search_data=keyword)

@app.route("/show/data23",methods=["GET", "POST"])
def render23():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data23 = collection23.find().skip(skip=skip).limit(per_page)
    total = collection23.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('religion_basic.html', data23=data23,pagination=pagination)
###############################################################################################################24
#data24数据,各国宗教信仰搜索功能
@app.route('/search/data24', methods=['GET', 'POST'])
def data_search24():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'国家编号':{'$regex': keyword, '$options': 'i'}},
            {'国家':{'$regex': keyword, '$options': 'i'}},
            {'编号':{'$regex': keyword, '$options': 'i'}},
            {'宗教':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search24 = collection24.find(query).skip(skip=skip).limit(per_page)
    total = collection24.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('religion_world.html', data24=list(data_search24),pagination=pagination,search_data=keyword)

@app.route("/show/data24",methods=["GET", "POST"])
def render24():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data24 = collection24.find().skip(skip=skip).limit(per_page)
    total = collection24.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('religion_world.html', data24=data24,pagination=pagination)
###############################################################################################################25
#data25数据,政党政策及影响信息搜索功能
@app.route('/search/data25', methods=['GET', 'POST'])
def data_search25():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'国家编号':{'$regex': keyword, '$options': 'i'}},
            {'国家':{'$regex': keyword, '$options': 'i'}},
            {'党派编号':{'$regex': keyword, '$options': 'i'}},
            {'党派':{'$regex': keyword, '$options': 'i'}},
            {'主要政策':{'$regex': keyword, '$options': 'i'}},
            {'社会影响':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search25 = collection25.find(query).skip(skip=skip).limit(per_page)
    total = collection25.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('Political_policy.html', data25=list(data_search25),pagination=pagination,search_data=keyword)

@app.route("/show/data25",methods=["GET", "POST"])
def render25():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data25 = collection25.find().skip(skip=skip).limit(per_page)
    total = collection25.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('Political_policy.html', data25=data25,pagination=pagination)
###############################################################################################################26
#data26数据,经济势力信息搜索功能
@app.route('/search/data26', methods=['GET', 'POST'])
def data_search26():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'国家编号':{'$regex': keyword, '$options': 'i'}},
            {'国家':{'$regex': keyword, '$options': 'i'}},
            {'领域编号':{'$regex': keyword, '$options': 'i'}},
            {'经济领域':{'$regex': keyword, '$options': 'i'}},
            {'主要企业':{'$regex': keyword, '$options': 'i'}},
            {'贸易伙伴':{'$regex': keyword, '$options': 'i'}},
            {'经济政策':{'$regex': keyword, '$options': 'i'}},
            {'经济势力':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search26 = collection26.find(query).skip(skip=skip).limit(per_page)
    total = collection26.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('economy.html', data26=list(data_search26),pagination=pagination,search_data=keyword)

@app.route("/show/data26",methods=["GET", "POST"])
def render26():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data26 = collection26.find().skip(skip=skip).limit(per_page)
    total = collection26.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('economy.html', data26=data26,pagination=pagination)
###############################################################################################################27
#data27数据,历史沿革数据搜索功能
@app.route('/search/data27', methods=['GET', 'POST'])
def data_search27():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'事件编号':{'$regex': keyword, '$options': 'i'}},
            {'事件名称':{'$regex': keyword, '$options': 'i'}},
            {'国家编号':{'$regex': keyword, '$options': 'i'}},
            {'国家':{'$regex': keyword, '$options': 'i'}},
            {'时间线编号':{'$regex': keyword, '$options': 'i'}},
            {'历史时间线':{'$regex': keyword, '$options': 'i'}},
            {'时间线具体事件':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search27 = collection27.find(query).skip(skip=skip).limit(per_page)
    total = collection27.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('history.html', data27=list(data_search27),pagination=pagination,search_data=keyword)

@app.route("/show/data27",methods=["GET", "POST"])
def render27():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data27 = collection27.find().skip(skip=skip).limit(per_page)
    total = collection27.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('history.html', data27=data27,pagination=pagination)
###############################################################################################################28
#data28数据,对于事件各国的立场搜索功能
@app.route('/search/data28', methods=['GET', 'POST'])
def data_search28():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'冲突事件':{'$regex': keyword, '$options': 'i'}},
            {'美国':{'$regex': keyword, '$options': 'i'}},
            {'日本':{'$regex': keyword, '$options': 'i'}},
            {'新加坡':{'$regex': keyword, '$options': 'i'}},
            {'印度':{'$regex': keyword, '$options': 'i'}},
            {'澳大利亚':{'$regex': keyword, '$options': 'i'}},
            {'中国':{'$regex': keyword, '$options': 'i'}},
            {'欧洲联盟':{'$regex': keyword, '$options': 'i'}},
            {'菲律宾':{'$regex': keyword, '$options': 'i'}},
            {'苏联':{'$regex': keyword, '$options': 'i'}},
            {'越南':{'$regex': keyword, '$options': 'i'}},
            {'乌干达':{'$regex': keyword, '$options': 'i'}},
            {'坦桑尼亚':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search28 = collection28.find(query).skip(skip=skip).limit(per_page)
    total = collection28.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('standpoint.html', data28=list(data_search28),pagination=pagination,search_data=keyword)

@app.route("/show/data28",methods=["GET", "POST"])
def render28():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data28 = collection28.find().skip(skip=skip).limit(per_page)
    total = collection28.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('standpoint.html', data28=data28,pagination=pagination)

###############################################################################################################29
#data29数据,国际事件与冲突搜索功能
@app.route('/search/data29', methods=['GET', 'POST'])
def data_search29():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'编号':{'$regex': keyword, '$options': 'i'}},
            {'军事冲突':{'$regex': keyword, '$options': 'i'}},
            {'国家编号':{'$regex': keyword, '$options': 'i'}},
            {'冲突时间':{'$regex': keyword, '$options': 'i'}},
            {'时间线编号':{'$regex': keyword, '$options': 'i'}},
            {'原因':{'$regex': keyword, '$options': 'i'}},
            {'持续时间':{'$regex': keyword, '$options': 'i'}},
            {'参与冲突国家':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search29 = collection29.find(query).skip(skip=skip).limit(per_page)
    total = collection29.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('country_conflict.html', data29=list(data_search29),pagination=pagination,search_data=keyword)

@app.route("/show/data29",methods=["GET", "POST"])
def render29():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data29 = collection29.find().skip(skip=skip).limit(per_page)
    total = collection29.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('country_conflict.html', data29=data29,pagination=pagination)
###############################################################################################################30
#data30数据,贸易关系搜索功能
@app.route('/search/data30', methods=['GET', 'POST'])
def data_search30():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'编号':{'$regex': keyword, '$options': 'i'}},
            {'国家':{'$regex': keyword, '$options': 'i'}},
            {'对应关系国':{'$regex': keyword, '$options': 'i'}},
            {'联合军事演习':{'$regex': keyword, '$options': 'i'}},
            {'资源与技术共享':{'$regex': keyword, '$options': 'i'}},
            {'战略规划与协调':{'$regex': keyword, '$options': 'i'}},
            {'常设使馆与领馆':{'$regex': keyword, '$options': 'i'}},
            {'大使与外交官':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search31 = collection30.find(query).skip(skip=skip).limit(per_page)
    total = collection30.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('trade.html', data30=list(data_search31),pagination=pagination,search_data=keyword)

@app.route("/show/data30",methods=["GET", "POST"])
def render30():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data31 = collection30.find().skip(skip=skip).limit(per_page)
    total = collection30.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('trade.html', data30=data31,pagination=pagination)
###############################################################################################################31
#data31数据,国际关系搜索功能
@app.route('/search/data31', methods=['GET', 'POST'])
def data_search31():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'编号':{'$regex': keyword, '$options': 'i'}},
            {'国家':{'$regex': keyword, '$options': 'i'}},
            {'对应关系国':{'$regex': keyword, '$options': 'i'}},
            {'联合军事演习':{'$regex': keyword, '$options': 'i'}},
            {'资源与技术共享':{'$regex': keyword, '$options': 'i'}},
            {'战略规划与协调':{'$regex': keyword, '$options': 'i'}},
            {'常设使馆与领馆':{'$regex': keyword, '$options': 'i'}},
            {'大使与外交官':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search31 = collection31.find(query).skip(skip=skip).limit(per_page)
    total = collection31.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('world_relationship.html', data31=list(data_search31),pagination=pagination,search_data=keyword)

@app.route("/show/data31",methods=["GET", "POST"])
def render31():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data31 = collection31.find().skip(skip=skip).limit(per_page)
    total = collection31.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('world_relationship.html', data31=data31,pagination=pagination)
###############################################################################################################32
#data32数据,地缘政治地理信息数据搜索功能
@app.route('/search/data32', methods=['GET', 'POST'])
def data_search32():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'国家':{'$regex': keyword, '$options': 'i'}},
            {'靠近的水域及岛屿':{'$regex': keyword, '$options': 'i'}},
            {'地形类型':{'$regex': keyword, '$options': 'i'}},
            {'灾害频发情况':{'$regex': keyword, '$options': 'i'}},
            {'气候类型':{'$regex': keyword, '$options': 'i'}},
            {'周边国家':{'$regex': keyword, '$options': 'i'}},
            {'地理资源':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search34 = collection32.find(query).skip(skip=skip).limit(per_page)
    total = collection32.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('Geography.html', data32=list(data_search34),pagination=pagination,search_data=keyword)

@app.route("/show/data32",methods=["GET", "POST"])
def render32():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data34 = collection32.find().skip(skip=skip).limit(per_page)
    total = collection32.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('Geography.html', data32=data34,pagination=pagination)
###############################################################################################################33
#data33数据,国际政治（军事、经济）组织功能描述搜索功能
@app.route('/search/data33', methods=['GET', 'POST'])
def data_search33():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'网站名':{'$regex': keyword, '$options': 'i'}},
            {'从属国家':{'$regex': keyword, '$options': 'i'}},
            {'网站介绍':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search34 = collection33.find(query).skip(skip=skip).limit(per_page)
    total = collection33.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('International_organization.html', data33=list(data_search34),pagination=pagination,search_data=keyword)

@app.route("/show/data33",methods=["GET", "POST"])
def render33():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data34 = collection33.find().skip(skip=skip).limit(per_page)
    total = collection33.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('International_organization.html', data33=data34,pagination=pagination)
###############################################################################################################34
#data34数据,媒体网站说明搜索功能
@app.route('/search/data34', methods=['GET', 'POST'])
def data_search34():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'网站名':{'$regex': keyword, '$options': 'i'}},
            {'从属国家':{'$regex': keyword, '$options': 'i'}},
            {'网站介绍':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search34 = collection34.find(query).skip(skip=skip).limit(per_page)
    total = collection34.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('net_introduction.html', data34=list(data_search34),pagination=pagination,search_data=keyword)

@app.route("/show/data34",methods=["GET", "POST"])
def render34():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data34 = collection34.find().skip(skip=skip).limit(per_page)
    total = collection34.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('net_introduction.html', data34=data34,pagination=pagination)


###########################################################################################36
#data36数据,人物、组织、媒体（外部数据）搜索功能
@app.route('/search/data36', methods=['GET', 'POST'])
def data_search36():
    keyword = request.args.get('keyword')    
    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    query = {'$or':
        [
            {'站点中文名':{'$regex': keyword, '$options': 'i'}},
            {'站点英文名':{'$regex': keyword, '$options': 'i'}},
            {'内容':{'$regex': keyword, '$options': 'i'}},
            {'作者':{'$regex': keyword, '$options': 'i'}},
            {'网站分类':{'$regex': keyword, '$options': 'i'}}
        ]
        }
    # 根据关键字查询数据
    data_search36 = collection36.find(query).skip(skip=skip).limit(per_page).sort("发表时间", -1)
    total = collection36.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('external_data.html', data36=list(data_search36),pagination=pagination,search_data=keyword)
@app.route("/show/data36",methods=["GET", "POST"])
def render36():    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    data5 = collection36.find().skip(skip=skip).limit(per_page).sort("发表时间", -1)
    total = collection36.count_documents({})
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('external_data.html', data36=data5,pagination=pagination)

@app.route('/data36/date_search', methods=['get','POST'])
def date36_search():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # 每页显示的数据量
    per_page = 10
    skip = (page - 1) * per_page
    selected_date_str = request.args.get['date']
    # selected_date = datetime.strftime(selected_date_str, '%Y-%m-%d').date()
    query = {"发表时间":{'$regex': selected_date_str, '$options': 'i'}}
    matched_events = collection36.find(query).skip(skip=skip).limit(per_page).sort("发表时间", -1)
    total = collection36.count_documents(query)
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('external_data.html',data5=matched_events, pagination=pagination, selected_date=selected_date_str)



app.run(host='0.0.0.0')