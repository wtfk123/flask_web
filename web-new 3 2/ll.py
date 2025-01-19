import pandas as pd
from pymongo import MongoClient

# 连接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['net_army']  # 替换为你的数据库名称
collection = db['各国贸易关系']  # 替换为你的集合名称

# 读取 Excel 文件
excel_file = '/home/bigdata/基础数据.xlsx'  # 替换为你的 Excel 文件路径
sheet_name = '贸易关系'  # 替换为你要读取的工作表名称

# 读取指定的工作表
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# 将数据插入 MongoDB
data = df.to_dict(orient='records')  # 将 DataFrame 转换为字典列表
collection.insert_many(data)

print("数据已成功导入 MongoDB")