from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Items',
                'price': 15.99
            }
        ]
    }
]


@app.route('/')
def home():
    return render_template('index.html')


# from server perspective
# POST - used to receive data
# GET - used to send data back only

# GET /store
@app.route('/store')
def get_stores():
    response_object = {}
    response_object['stores'] = stores
    return jsonify(response_object)


# GET /store/<string:name>
@app.route('/store/<string:name>')  # 'http:127.0.0.1/store/some_name'
def get_store(name):
    # Inerate over stores
    for store in stores:
        # if the store name matches, return it
        if store['name'] == name:
            return jsonify(store)
    # if none mathes, retyrn an error message
    return jsonify({'message': 'store not found'})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})


# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# POST /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})


if __name__ == '__main__':
    app.run(port=5001)
