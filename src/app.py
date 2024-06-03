from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()
    input_text = data['input_text']

    # process.pyを実行し、結果を取得する
    result = subprocess.run(['python', 'process.py', input_text], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip().split('\n')
    error = result.stderr.decode('utf-8').strip()

    if error:
        return jsonify({'error': error}), 400

    return jsonify({'result': output[0], 'original': output[1]})

if __name__ == '__main__':
    app.run(debug=True)