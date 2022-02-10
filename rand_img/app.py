import os
import random
from flask import Flask, send_file

app = Flask(__name__)
IMG_PATH = os.path.join(os.path.dirname(__file__), '../image')

@app.route("/", methods=['GET'])
def home():
    files = os.listdir(IMG_PATH)
    num = random.randint(0, len(files)-1)

    filename = files[num]
    file_path = os.path.join(IMG_PATH, filename)

    return send_file(file_path, download_name=filename, mimetype='image/jpeg')

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    #app.run(debug=True)