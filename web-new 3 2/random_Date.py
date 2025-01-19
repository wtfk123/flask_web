import pymongo
import random
from datetime import datetime, timedelta

# 连接到 MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['net_army']  # 替换为你的数据库名
collection = db['推特推文']  # 替换为你的集合名

# 定义日期范围
start_date = datetime(2024, 5, 10)
end_date = datetime(2024, 9, 30)

# 计算日期范围的天数
date_range = (end_date - start_date).days

# 更新集合中的每个文档
for document in collection.find():
    # 生成随机日期
    random_days = random.randint(0, date_range)
    random_date = start_date + timedelta(days=random_days)
    
    # 更新文档中的 date 字段
    collection.update_one(
        {'_id': document['_id']},
        {'$set': {'tweetDate': random_date.strftime('%Y-%m-%d')}}
    )

print("Date fields updated successfully.")