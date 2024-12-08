from flask import Flask, request, jsonify
from status import Status

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the API'}), 200

@app.route('/status', methods=['GET'])
def status():
    task_id = request.args.get('task_id')
    if not task_id:
        return jsonify({'error': 'task_id is required'}), 400
    status = Status.get_status(task_id)
    return jsonify(status)

@app.route('/all_status', methods=['GET'])
def all_status():
    statuses = Status.get_all_status()
    return jsonify(statuses)

if __name__ == '__main__':
    app.run(debug=True)
