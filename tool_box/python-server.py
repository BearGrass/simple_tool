from flask import Flask, request, jsonify
import importlib

app = Flask(__name__)

@app.route('/run_tool', methods=['POST'])
def run_tool():
    data = request.json
    tool_name = data['tool']
    params = data['params']
    
    try:
        module = importlib.import_module(f'src.python.{tool_name}')
        result = module.run(params)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)