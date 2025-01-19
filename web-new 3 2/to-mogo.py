from pymongo import MongoClient

# 连接到MongoDB
client = MongoClient("mongodb://localhost:27017/your_database")  # 替换为您的MongoDB URI
db1 = client['ZT']  # 替换为您的数据库名称
db2 = client['net_army']  # 替换为您的数据库名称

# 指定源集合和目标集合
source_collection = db1['media']  # 替换为您的源集合名称
target_collection = db2['多模态数据']  # 替换为您的目标集合名称

# 从源集合中获取所有文档
documents = source_collection.find()

# 将文档插入到目标集合
# 这里可以选择性地处理文档，例如只复制特定字段
for doc in documents:
    target_collection.insert_one(doc)  # 插入文档到目标集合

print("数据已成功导入到目标集合。")