from test import data_process
import json
from py2neo import Graph
import subprocess

def start_neo4j():
    try:
        # 假设Neo4j安装在默认路径，调整为你的实际安装路径
        neo4j_start_command = "/usr/vis_world/neo4j-community-4.4.28/bin/neo4j start"
        subprocess.run(neo4j_start_command, check=True, shell=True)
        print("Neo4j has been started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Neo4j: {e}")



list1=['鲍照',
 '陈叔宝',
 '何逊',
 '沈约',
 '萧纲',
 '萧统',
 '萧衍',
 '谢安',
 '谢朓',
 '颜延之',
 '陈沂',
 '陈子龙',
 '方孝孺',
 '高启',
 '顾起元',
 '黄周星',
 '解缙',
 '李贽',
 '刘基',
 '宋濂',
 '王世贞',
 '吴伟业',
 '夏完淳',
 '余怀',
 '钟惺',
 '周济',
 '李渔',
 '龚贤',
 '吴敬梓',
 '袁枚',
 '王贞仪',
 '梅曾亮',
 '魏源',
 '汪士铎',
 '陈作霖',
 '杜牧',
 '冯延巳',
 '郭茂倩',
 '李白',
 '李煜',
 '刘禹锡',
 '王安石',
 '徐铉',
 '许嵩',
 '张祜',
 '周应合',
 '盛时泰',
 '朱元璋',
 '焦竑',
 '高岑']
list=[
 '高启',
 '顾起元',
 '黄周星',
 '解缙',
 '李贽',
 '刘基',
 '宋濂',
 '王世贞',
 '吴伟业',
 '夏完淳',
 '余怀',
 '钟惺',
 '周济',
 '李渔',
 '龚贤',
 '吴敬梓',
 '袁枚',
 '王贞仪',
 '梅曾亮',
 '魏源',
 '汪士铎',
 '陈作霖',
 '杜牧',
 '冯延巳',
 '郭茂倩',
 '李白',
 '李煜',
 '刘禹锡',
 '王安石',
 '徐铉',
 '许嵩',
 '张祜',
 '周应合',
 '盛时泰',
 '朱元璋',
 '焦竑',
 '高岑']

# 调用函数启动Neo4j
start_neo4j()

graph = Graph("https://47.108.164.230:7474/browser", user="neo4j", password="123456", name="neo4j")

query = f"""MATCH (p1:author)-[:包含人物|作者]-(w:article)-[:包含人物|作者]-(p2:author)
WHERE p1.author_name IN {list} AND p2.author_name IN {list}
MERGE (p1)-[:CO_AUTHORED_WITH]->(p2)
RETURN p1, p2"""


result = graph.run(query)
"""with open('result.txt', 'w', encoding='utf-8') as file:
 for record in result:
  print(record)
  file.write(str(record) + '\n')"""
unique_records = set()

for record in result:
  if(record['p1']==record['p2']):
   continue
  unique_records.add((record['p1'], record['p2']))

    # 将集合转换为列表（如果需要的话）
#unique_records_list = list(unique_records)
print(unique_records)
"""with open('result2.txt', 'w', encoding='utf-8') as file:
 for record in unique_records:
  print(record)
  file.write(str(record) + '\n')"""

current_id = 0
name_id_mapping = {}
def convert_node_to_dict(node):
 global current_id
 global name_id_mapping

 author_name = node['author_name']

 # 如果人名已经在映射中，则使用已分配的ID
 if author_name in name_id_mapping:
  converted_dict = {"id": name_id_mapping[author_name], "name": author_name, "dynasty": node['dynasty']}
 else:
  # 否则，分配新ID并更新映射
  converted_dict = {"id": current_id, "name": author_name, "dynasty": node['dynasty']}
  name_id_mapping[author_name] = current_id
  current_id += 1

 return converted_dict
def convert_result_to_list(result_set):
 global current_id
 global name_id_mapping

 converted_list = []

 for nodes_tuple in result_set:
  converted_pair = tuple(map(convert_node_to_dict, nodes_tuple))
  converted_list.append(converted_pair)

 return converted_list
converted_result = convert_result_to_list(unique_records)


def extract_nodes_from_result(result_list):
 unique_nodes = {}  # 使用字典来确保节点的唯一性

 for nodes_tuple in result_list:
  for node_dict in nodes_tuple:
   # 提取节点信息
   node_id = node_dict['id']
   node_name = node_dict['name']
   node_dynasty = node_dict['dynasty']

   # 使用 (name, dynasty) 作为键来判断节点是否已经存在
   key = (node_name, node_dynasty)

   # 如果节点不存在，则添加到字典中
   if key not in unique_nodes:
    unique_nodes[key] = {'id': node_id, 'name': node_name, 'dynasty': node_dynasty}

 # 将字典的值转换为列表


 return unique_nodes
node_result = extract_nodes_from_result(converted_result)
print(converted_result)
print(node_result)

