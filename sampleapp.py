# Flaskライブラリから必要なモジュールをインポート
from flask import Flask, jsonify, request, render_template

# アプリケーション本体を作成
# 「__name__」・・・特別なデフォルト変数で今回でいうと「sampleapp」にあたる
app = Flask(__name__)

# 仮のDB
stores = [
    {
        'name':'my_store',
        'items':[
            {
                'name':'chocolate',
                'price':120,
            }
        ]
    }
]

# storeに対するCRUD-----------------------

# GETメソッド
# appにURIを登録
@app.route('/stores/<string:name>') # 'http://127.0.0.1:5000/store/some_name'
# 「jsonify()」・・・辞書型からjson型を作成する
# 引数にURI中の<string:name>を代入
def get_store(name):
    for store in stores:
        if store['name']== name:
            return jsonify(store)
    return jsonify({'message':'no store named {} found.'.format(name)})


# POST
@app.route('/stores', methods=['POST'])
def create_store():
    # request.get_json()でリクエストボディを取得
    request_data = request.get_json()
    store = next(filter(lambda x: x['name']==request_data['name'], stores), None)
    if store != None:
        return jsonify({'message':'store named {} already exist.'.format(request_data['name'])})
    else:
        new_store = {
            'name':request_data['name'],
            'items':request_data['items']
        }
        stores.append(new_store)
        return jsonify({'message':'{} store is added'.format(request_data['name'])})
    

# PUT
@app.route('/stores/<string:name>', methods=['PUT'])
def update_store(name):
    request_data = request.get_json()
    store = next(filter(lambda x: x['name']==name, stores), None)
    if store == None:
        return jsonify({'massage':'no store named {} found.'.format(name)})
    else:
        store['items'] = request_data['items']
        return jsonify({'massage':'{} is updated.'.format(name)})
  
    
# DELETE
@app.route('/stores')
def get_stores():
    return jsonify({'stores':stores})


# ホーム画面にhtmlを読み込んでみる。
# GET /
@app.route('/')
def home():
    return render_template("index.html")

# ポート番号（5000がデフォルト）
# 他のポート番号も指定できます。
app.run(port=5000)