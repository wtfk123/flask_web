from pymongo import MongoClient
from datetime import datetime

client=MongoClient('mongodb://localhost:27017')
db=client['net_army']
collection = db['多模态数据']

# 查询所有需要更新的文档
documents = collection.find({"tweetDate": {"$exists": True}}) 


for doc in documents:
    original_time = doc['tweetDate']  # 获取原始时间字符串
    # 转换时间格式
    try:
        # 将原始字符串转换为 datetime 对象
        dt = datetime.strptime(original_time,  "%a %b %d %H:%M:%S %z %Y")
        # 格式化为新的字符串格式
        new_time = dt.strftime('%Y-%m-%d')
        
        # 更新文档
        collection.update_one({'_id': doc['_id']}, {'$set': {'tweetDate': new_time}})  # 替换为您的时间字段名称
        
    except:
        pass