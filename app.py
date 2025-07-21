from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user store
users = {}
user_id_counter = 1

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask User API. Use /users endpoint."})

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    user = {
        'id': user_id_counter,
        'name': data['name']
    }
    users[user_id_counter] = user
    user_id_counter += 1
    return jsonify(user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    user['name'] = data['name']
    users[user_id] = user
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    del users[user_id]
    return jsonify({'message': 'User deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
