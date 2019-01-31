from flask import redirect,render_template,jsonify,request
from test_manage import testManage_app
import requests



@testManage_app.route("/api")
def api():
    return render_template("test_manage/index.html")


@testManage_app.route("/test",methods=["POST"])
def test():
    msg = {}
    params = request.form
    url = params.get("url")
    method = params.get("method")
    userAgent = params.get("userAgent")
    keys = params.get("keys").split(",")
    values = params.get("values").split(",")
    data = {}
    requestsParams = {}
    requestsParams["url"] = url
    if userAgent:
        requestsParams["headers"] = {"user-agent": userAgent}
    if keys:
        for i in range(len(keys)):
            if keys[i]:
                data[keys[i]] = values[i]
    if method == "GET":
        requestsParams["params"] = data
        response = requests.get(**requestsParams).json()
        msg["code"] = 0
        msg["response"] = response
    elif method == "POST":
        requestsParams["data"] = data
        response = requests.post(**requestsParams).json()
        msg["code"] = 0
        msg["response"] = response
    else:
        msg = {"code":1001,"msg":"参数有误！"}
    return jsonify(msg)