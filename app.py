from flask import Flask , redirect, request, jsonify
app = Flask(__name__,
    static_url_path='',
    static_folder='web/static',
    template_folder='web/templates')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def root():
    return redirect("/index.html")

@app.route('/ping', methods=['POST'])
def ping():
    print(request.form)
    return (jsonify(Ping="pong"),200)
    
if __name__ == '__main__':
    app.run(debug=True,port=8080)


