from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
from socket import gethostname
# from netifaces import interfaces, ifaddresses, AF_INET
import os

app = Flask(__name__)
CORS(app)

r_flag = True
ip = None
hostname = None


@app.route("/")
def index():
    global ip
    print(ip)
    return render_template("index.html", ip_addr=ip, host=hostname)


@app.route("/api/v1")
def index_route():
    return {"message": "Hi there!, you are at index route"}, 200


@app.route("/api/v1/greet")
def greet():
    global r_flag
    return {"node": hostname, "receive": r_flag}, 200


@app.route("/api/v1/receive", methods=["GET", "POST", "PUT"])
def receive():
    global r_flag
    filenames = []
    if request.method == "GET":
        return render_template("send.html", ip_addr=ip, host=hostname)
    if request.method == "POST" and r_flag == True:
        for f in request.files.getlist(key="files"):
            filename = secure_filename(f.filename)
            filenames.append(filename)
            f.save(os.path.join("./received_files", filename))
        return {
            "message": "Received successfully",
            "filenames": filenames,
            "sending_node": ip,
            "receiving_node": hostname
        }, 200
    if request.method == "PUT":
        data = request.get_json()
        r_flag = data["receive_flag"]
        return {"message": F"Toggled receive flag to {r_flag}"}, 200
    return {"message": "Invalid request"}, 400


def get_ip_and_host():
    #     global ip
    global hostname
    hostname = gethostname()
#     for ifaceName in interfaces():
#         addresses = [i['addr'] for i in ifaddresses(
#             ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
#         if addresses[0] is not None and "192" in addresses[0]:
#             ip = addresses[0]


if __name__ == "__main__":
    get_ip_and_host()
    app.run(debug=True, port=9999, host="0.0.0.0")
