from flask import Flask, request, jsonify, render_template
from py2neo import Graph
from test import data_process
import sqlite3
app = Flask(__name__)
app.static_folder = 'static'

#app.template_folder = 'templates/Vis_Course/vis_course_v4'

@app.route('/')
def index():
    return render_template('vis_course_v4/index.html')

@app.route('/page2.html')
def page2():
    return render_template('vis_course_v4/page2.html')

@app.route('/map&inf.html')
def map():
    return render_template('vis_course_v4/map&inf.html')

@app.route('/page_base.html')
def page_base():
    return render_template('vis_course_v4/page_base.html')


@app.route('/process_request', methods=['POST'])
def process_request():
    # 从前端获取 JSON 数据
    data = request.get_json()
    print(data)
    if data is not None:
        # 获取四个变量
        character = data.get('character', '')
        dynasty = data.get('dynasty', '')
        literary_style = data.get('literary_style', '')
        location = data.get('location', '')

        node,relation = data_process(character, dynasty, literary_style, location)

        response_data = {
            "node": node,
            "relation": relation,
            "additional_info": "This is additional information."
        }
        print(response_data)
        return jsonify(response_data)

    return jsonify({"error": "Invalid data"})
@app.route('/search', methods=['GET'])
def page2_process():
    #data = request.get_json()
    search_query = request.args.get('q', '')
    vis_db = sqlite3.connect('static/database/vis.db')
    cursor = vis_db.cursor()
    query1="SELECT * from author join cal_grade ON author.a_id = cal_grade.a_id where author.a_name =?"
    query2 = "SELECT * from author join grade ON author.a_id = grade.a_id where author.a_name =?"
    cursor.execute(query1, (search_query,))
    result = cursor.fetchall()
    cursor.execute(query2, (search_query,))
    res=cursor.fetchall()
    print(search_query)
    # description=f"{search_query},{res[0][2]}代诗人,作品{res[0][4]}篇，覆盖{res[0][8]}种文体，相关作品{res[0][5]}篇，相关人物{res[0][6]}位，相关地点{res[0][7]}个."
    response_data = {
        # "des":description,
        "scores": result[0][4:],
        "name":result[0][1]
    }
    return jsonify(response_data)

@app.route('/select', methods=['POST'])
def page_base_process():
    data = request.get_json()
    vis_db = sqlite3.connect('static/database/vis.db')
    cursor = vis_db.cursor()
    query="select wuy,wen,shi,ji,poe,qu,qiy,bea,fu,ci from dynasty where dynasty=?"
    cursor.execute(query, (data['option1'],))
    result = cursor.fetchall()
    cursor.execute(query, (data['option2'],))
    res = cursor.fetchall()
    response_data = {
        "option1": result[0],
        "option2": res[0],
        "name1":data['option1'],
        "name2":data['option2']
    }
    print(response_data)
    return jsonify(response_data)
def process_data(character, dynasty, literary_style, location):
    result = {
        "character": character,
        "dynasty": dynasty,
        "literary_style": literary_style,
        "location": location
    }
    return result

if __name__ == '__main__':
    #node, relation = data_process(character="李白")
    #print(node)
    #print(relation)
    app.run(host='0.0.0.0',port=80)
