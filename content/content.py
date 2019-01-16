from flask import render_template,redirect,jsonify,request,session
from content import content_app
import dao,models,decorator
import time,hashlib,os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "/static/upload/"
ALLOW_EXENSIONS = ["txt","pdf","png","jpg","jpeg","gif"]


@content_app.route("/catalog",endpoint="catalog")
@decorator.authentication
def cataLog():
    return render_template("content/catalog.html")


@content_app.route("/getCatalog",methods=["GET","POST"],endpoint="getCatalog")
@decorator.authentication
def getCatalog():
    msg = {}
    msg["data"] = []
    if request.method == "GET":
        params = request.args
        parentId = params.get("parentId")
        file = models.db.session.query(models.ContentFile).filter(models.ContentFile.delete_flag==0,models.ContentFile.parent==parentId).all()
        msg["parent"] = parentId
    else:
        params = request.form
        parentId = params.get("parentId")
        if parentId != "-1":
            parentFile = models.db.session.query(models.ContentFile).filter(models.ContentFile.delete_flag==0,models.ContentFile.pk_id==parentId).first()
            parent = parentFile.parent
        else:
            parent = -1
        file = models.db.session.query(models.ContentFile).filter(models.ContentFile.delete_flag==0,models.ContentFile.parent==parent).all()
        msg["parent"] = parent
    folder = []
    html = []
    image = []
    for item in file:
        type = item.type
        if type == 0:
            appendInfo = {
                "fileId": item.pk_id,
                "fileName": item.name,
                "type": type
            }
            folder.append(appendInfo)
        elif type == 1:
            appendInfo = {
                "fileId": item.pk_id,
                "fileName": item.name,
                "type": type
            }
            html.append(appendInfo)
        else:
            appendInfo = {
                "fileId": item.pk_id,
                "fileName": item.name,
                "type": type,
                "des": item.des
            }
            image.append(appendInfo)
    msg["data"] = folder + html + image
    # 返回一个icon列表，列表下标和content_file.type相匹配
    icon = models.db.session.query(models.BusinessKeyWord).filter(models.BusinessKeyWord.key=="cataLogIcon").first().value.split(",")
    msg["icon"] = icon
    msg["code"] = 0
    msg["msg"] = "请求成功！"
    return jsonify(msg)

@content_app.route("/addFile",methods=["GET","POST"],endpoint="addFile")
@decorator.authentication
def addFile():
    msg = {}
    msg["data"] = []
    if request.method == "GET":
        params = request.args
        parentId = params.get("parentId")
        content = {
            "parentId": parentId
        }
        return render_template("content/addFile.html",content=content)
    else:
        params = request.form
        parentId = params.get("parentId")
        fileName = params.get("fileName")
        fileType = int(params.get("fileType"))
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        if fileType == 0:
            newFile = models.ContentFile(name=fileName,parent=parentId,type=fileType,create_time=now,update_time=now)
            models.db.session.add(newFile)
            models.db.session.commit()
            msg["code"] = 0
            msg["msg"] = "添加成功！"
        elif fileType == 1:
            contentHtml = params.get("des")
            newFile = models.ContentFile(name=fileName, parent=parentId, type=fileType, create_time=now, des=contentHtml, update_time=now)
            models.db.session.add(newFile)
            models.db.session.commit()
            msg["code"] = 0
            msg["msg"] = "添加成功！"
        elif fileType == 2:
            imgSrc = params.get("des")
            imgName = params.get("imageName")
            newFile = models.ContentFile(name=imgName, parent=parentId, type=fileType, create_time=now,des=imgSrc, update_time=now)
            models.db.session.add(newFile)
            models.db.session.commit()
            msg["code"] = 0
            msg["msg"] = "添加成功！"
        else:
            msg["code"] = 1001
            msg["msg"] = "你走开！！！"
        return jsonify(msg)


@content_app.route("/content")
@decorator.authentication
def content():
    msg = {}
    msg["data"] = []
    params = request.args
    fileId = params.get("fileId")
    file = models.db.session.query(models.ContentFile).filter(models.ContentFile.pk_id == fileId,models.ContentFile.delete_flag == 0).first()
    return render_template("content/content.html",content=file)

@content_app.route("/openCatalog",methods=["POST"],endpoint="openCatalog")
@decorator.authentication
def openCatalog():
    msg = {}
    msg["data"] = []
    params = request.form
    fileId = params.get("fileId")
    file = models.db.session.query(models.ContentFile).filter(models.ContentFile.pk_id==fileId,models.ContentFile.delete_flag==0).first()
    fileType = file.type
    if fileType == 0:
        pass
    elif fileType == 1:
        msg["url"] = "/content/content?fileId="+fileId
    elif fileType ==2:
        msg["src"] = file.des
    return jsonify(msg)

@content_app.route("/uploadFile",methods=["POST"],endpoint="uploadFile")
@decorator.authentication
def uploadFile():
    if request.method == "POST":
        msg = {}
        f = request.files["file"]
        fileName = secure_filename(f.filename)
        suffix = fileName.split(".")[-1]
        now = int(time.time()*1000)
        name = str(now)+"."+suffix
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, '../static/upload/image',name)
        f.save(upload_path)
        msg["code"] = 0
        msg["msg"] = "上传成功！"
        msg["data"] = {
            "src": "/static/upload/image/"+name
            ,"title": fileName
        }
        return jsonify(msg)