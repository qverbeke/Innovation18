from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST'])
def result():
    data =dict(request.form)
    print(data)
    return ('',201)

if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True,port=6969)

