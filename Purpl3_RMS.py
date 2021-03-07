from flask import Flask , redirect, request, jsonify
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/ping', methods=['POST'])
def ping():
    print("ping request: ", request.json)
    return (jsonify(Ping="pong"),200)

@app.route('/api', methods=['POST'])
def apiRequest():
    print("api request: ", request.json)
    return (jsonify(ErrorCode=0),200)

@app.route('/login', methods=['POST'])
def loginRequest():
    print("login request: ", request.json)
    return (jsonify(ErrorCode=0),200)

    
if __name__ == '__main__':
    app.run(debug=True,port=8080)

