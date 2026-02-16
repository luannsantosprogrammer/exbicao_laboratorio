from flask import Flask,request, jsonify
import logging


app = Flask(__name__)


status = {"status": "aguardando"}

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) # Só vai mostrar logs se houver erro




@app.route('/status', methods=['POST'])
def servidos_post():
    resposta = request.get_json()
    status['status'] = resposta.get('status','aguardando')
    return jsonify(status)


@app.route('/status', methods=['GET'])
def servidos_get():
    return jsonify(status)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
