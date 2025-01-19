import os
import pandas as pd
from pymongo import MongoClient

# 连接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')  # 根据需要修改连接字符串
db = client['net_army']  # 替换为您的数据库名称
collection = db['和平团结']  # 替换为您的集合名称

# 指定要读取的文件夹路径
folder_path = '/media/bigdata/Elements/和平团结-2024/'  # 替换为您的文件夹路径

# 遍历文件夹中的所有 Excel 文件
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        file_path = os.path.join(folder_path, filename)
        
        # 读取 Excel 文件
        df = pd.read_excel(file_path)

        # 将 DataFrame 中的数据插入 MongoDB
        data_to_insert = df.to_dict(orient='records')  # 转换为字典列表
        if data_to_insert:
            collection.insert_many(data_to_insert)
            print(f"成功插入文件 {filename} 中的 {len(data_to_insert)} 条记录。")
        else:
            print(f"文件 {filename} 中没有可插入的数据。")

print("所有文件处理完成。")
"""import pandas as pd
from pymongo import MongoClient

# 连接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')  # 根据需要修改连接字符串
db = client['net_army']  # 替换为您的数据库名称
collection = db['媒体']  # 替换为您的集合名称

# 读取 Excel 文件
excel_file_path = '/media/bigdata/Elements/采集数据/媒体/媒体数据/媒体_0705_001/媒体_0705_001_8.csv'  # 替换为您的 Excel 文件路径
df = pd.read_excel(excel_file_path)

# 将 DataFrame 中的数据插入 MongoDB
data_to_insert = df.to_dict(orient='records')  # 转换为字典列表
collection.insert_many(data_to_insert)

print(f"成功插入 {len(data_to_insert)} 条记录到 MongoDB。")"""