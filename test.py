from py2neo import Graph
from py2neo.cypher import encoding
import json

def query_knowledge_graph(character=None, dynasty=None, literary_style=None, location=None):

    graph = Graph("https://[your_own_IP_address]/browser", user="user_name", password="user_codes",name="user_database")

    query = "MATCH (article)"
    where_conditions = []

    if character:
        where_conditions.append(f"(article)-[:包含人物]->(:author {{author_name: '{character}'}})")
    if dynasty:
        where_conditions.append(f"(article)-[:朝代]->(:dynasty {{dynasty: '{dynasty}'}})")
    if literary_style:
        where_conditions.append(f"(article)-[:文体]->(:style {{article_style: '{literary_style}'}})")
    if location:
        where_conditions.append(f"(article)-[:相关地点]->(:place {{place: '{location}'}})")

    if where_conditions:
        query += " WHERE " + " AND ".join(where_conditions)
    query+="""
              OPTIONAL MATCH (article)-[]-(place:place)
              OPTIONAL MATCH (article)-[]-(author:author)
              OPTIONAL MATCH (article)-[]-(dynasty:dynasty)
              OPTIONAL MATCH (article)-[]-(style:style)
              """

    query += " RETURN article,author,dynasty,style,place"


    result = graph.run(query)

    results_list = [record["article"] for record in result]

    return results_list
def deduplicate_json_results(json_results, key="article_id"):
    unique_keys = set()
    deduplicated_results = []

    for result in json_results:
        value = result[key]
        if value not in unique_keys:
            unique_keys.add(value)
            deduplicated_results.append(result)

    return deduplicated_results


def process_json_to_nodes_and_edges(data):
    unique_entities = {}
    nodes = []
    edges = []

    def get_unique_id(value, unique_dict):
        if value not in unique_dict:
            unique_dict[value] = len(unique_dict)
        return unique_dict[value]

    for record in data:
        relevant_places = record.get('relevant_place').split(',')
        article_style = record.get('article_style')
        dynasty = record.get('dynasty')
        article_name = record.get('article_name')
        author_name = record.get('author_name')

        author_id = get_unique_id(author_name, unique_entities)
        dynasty_id = get_unique_id(dynasty, unique_entities)
        article_style_id = get_unique_id(article_style, unique_entities)
        article_name_id = get_unique_id(article_name, unique_entities)

        for place in relevant_places:
            place_id = get_unique_id(place, unique_entities)
            nodes.append({'id': place_id, 'name': place})
            edges.append({'source': article_name_id, 'target': place_id})

        nodes.append({'id': author_id, 'name': author_name})
        nodes.append({'id': dynasty_id, 'name': dynasty})
        nodes.append({'id': article_style_id, 'name': article_style})
        nodes.append({'id': article_name_id, 'name': article_name})

        edges.append({'source': article_name_id, 'target': article_style_id})
        edges.append({'source': article_style_id, 'target': dynasty_id})
        edges.append({'source': dynasty_id, 'target': author_id})

    return nodes, edges
def deduplicate_nodes(nodes):
    unique_nodes = {}
    deduplicated_nodes = []

    nodes.sort(key=lambda x: x['id'])

    for node in nodes:
        node_id = node['id']
        if node_id not in unique_nodes:
            unique_nodes[node_id] = True
            deduplicated_nodes.append(node)

    return deduplicated_nodes


def generate_relationships(data, nodes):
    relationships = []

    name_to_id = {node['name']: node['id'] for node in nodes}

    relationship_id = 0

    for item in data:
        article_name = item['article_name']
        article_id = name_to_id.get(article_name, None)

        if article_id is not None:
            author_name = item['author_name']
            author_id = name_to_id.get(author_name, None)
            if author_id is not None:
                relationships.append(
                    {'id': relationship_id, 'source': article_id, 'target': author_id, 'relation': '作者',
                     'value': None})
                relationship_id += 1
            if 'relevant_author' in item:
                relevant_authors = item['relevant_author'].split(',')
                for relevant_author in relevant_authors:
                    relevant_author_id = name_to_id.get(relevant_author, None)
                    if relevant_author_id is not None:
                        relationships.append({'id': relationship_id, 'source': article_id, 'target': relevant_author_id,
                                              'relation': '相关人物', 'value': None})
                        relationship_id += 1

            if 'relevant_place' in item:
                relevant_places = item['relevant_place'].split(',')
                for relevant_place in relevant_places:
                    relevant_place_id = name_to_id.get(relevant_place, None)
                    if relevant_place_id is not None:
                        relationships.append({'id': relationship_id, 'source': article_id, 'target': relevant_place_id,
                                              'relation': '相关地点', 'value': None})
                        relationship_id += 1

            dynasty = item['dynasty']
            dynasty_id = name_to_id.get(dynasty, None)
            if dynasty_id is not None:
                relationships.append(
                    {'id': relationship_id, 'source': article_id, 'target': dynasty_id, 'relation': '朝代',
                     'value': None})
                relationship_id += 1

            article_style = item['article_style']
            article_style_id = name_to_id.get(article_style, None)
            if article_style_id is not None:
                relationships.append(
                    {'id': relationship_id, 'source': article_id, 'target': article_style_id, 'relation': '文体',
                     'value': None})
                relationship_id += 1

    return relationships


def process_nodes_to_custom_json(nodes):
    processed_nodes = [{'id': node['id'], 'name': node['name']} for node in nodes]
    return json.dumps(processed_nodes, ensure_ascii=False)

def process_relations_to_json(relations):
    processed_relations = [{'id': relation['id'], 'source': relation['source'], 'target': relation['target'], 'relation': relation['relation'], 'value': 1} for relation in relations]
    return json.dumps(processed_relations, ensure_ascii=False)

"""data=query_knowledge_graph(character="陈沂")
data= json.dumps(data, ensure_ascii=False)
data=json.loads(data)
data=deduplicate_json_results(json_results=data)
print(data)
node,edge=process_json_to_nodes_and_edges(data)
print(process_nodes_to_custom_json(deduplicate_nodes(node)))
relation=generate_relationships(data,deduplicate_nodes(node))
print(process_relations_to_json(relation))"""
def process_data(data, node):

    for item in node:
        if item['name'] in data:
            item['group'] =1
        elif item['name'] in ['诗', '词', '文集', '五言律诗', '传状文','文集','杂记文','七言律诗','道书','笔记文','诗集','文','类书','骈体文','小说','剧曲','五言古体诗','乐府诗','论说文','古体诗','赋','史书','纪传体史书','地方志','不详']:
            item['group']=6
        elif item['name'] in ['唐', '宋','明','清','南唐','晋','现当代','元','东晋','南朝','东吴']:
            item['group']=5
        elif '《' in item['name']:
            item['group'] = 2
        else:
            item['group']=3


    return node
def data_process(character=None, dynasty=None, literary_style=None, location=None):
    data = query_knowledge_graph(character=character,dynasty=dynasty,literary_style=literary_style,location=location)
    data = json.dumps(data, ensure_ascii=False)
    data = json.loads(data)
    data = deduplicate_json_results(json_results=data)
    node, edge = process_json_to_nodes_and_edges(data)
    list=[]
    node=deduplicate_nodes(node)
    relation = generate_relationships(data, node)
    node=process_nodes_to_custom_json(node)
    #print(node)
    node=json.loads(node)
    node = process_data([character, dynasty, literary_style, location], node)

    node=json.dumps(node, ensure_ascii=False)
    #print(node)
    relation=process_relations_to_json(relation)
    return node,relation

#print(edge)

