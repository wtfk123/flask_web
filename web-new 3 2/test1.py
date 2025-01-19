from pymongo import MongoClient
import random
from datetime import datetime, timedelta

# 连接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')  # 根据需要修改连接字符串
db = client['net_army']  # 替换为您的数据库名称
collection = db['推特推文']  # 替换为您的集合名称

# 从 MongoDB 中提取“发表时间”
documents = collection.find({}, {'tweetDate': 1})  # 只提取“发表时间”字段

# 定义日期范围
start_date = datetime(2024, 1, 30)
end_date = datetime(2024, 9, 30)

# 随机修改不在2024年1月30日到9月30日之间的“发表时间”
for doc in documents:
    if 'tweetDate' in doc:
        publish_date_str = doc['tweetDate']  # 获取字符串类型的 timestamp

        try:
            # 尝试解析日期，先尝试完整格式，然后尝试仅日期格式
            try:
                publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d')

            # 检查发表时间是否在指定范围内
            if publish_date < start_date or publish_date > end_date:
                # 生成一个随机的日期在2024年7月30日到9月30日之间
                random_start_date = datetime(2024, 1, 30)
                random_end_date = datetime(2024, 9, 30)
                random_date = random_start_date + timedelta(days=random.randint(0, (random_end_date - random_start_date).days))

                # 将新的日期格式化为字符串
                new_publish_date_str = random_date.strftime('%Y-%m-%d')

                # 更新MongoDB中的文档
                collection.update_one({'_id': doc['_id']}, {'$set': {'tweetDate': new_publish_date_str}})
                print(f"文档 {doc['_id']} 的发表时间更新为 {new_publish_date_str}")

        except ValueError as ve:
            print(f"处理文档 {doc['_id']} 时日期格式错误: {ve}")
        except Exception as e:
            print(f"处理文档 {doc['_id']} 时出错: {e}")

print("更新完成。")