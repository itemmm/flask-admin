from flask import render_template,redirect,jsonify,request,session
from manager import business_app
import dao,models,decorator
import time,hashlib



@business_app.route("/login",methods=["GET","POST"])
def login():
    msg = {}
    msg["data"] = []
    if request.method == "GET":
        systemName = dao.getSystemName()
        return render_template("manage/login.html",content=systemName)
    else:
        params = request.form
        loginName = params.get("loginName")
        passWord = params.get("passWord")
        user = dao.selectBusinessUserByLoginName(loginName=loginName)
        if user and user.password == passWord:
            session["loginName"] = user.login_name
            session["passWord"] = user.password
            session["nickName"] = user.nick_name
            msg["code"] = 0
            msg["msg"] = "请求成功！"
        else:
            msg["code"] = 1001
            msg["msg"] = "用户名或密码错误！"
        return jsonify(msg)

@business_app.route("/logout")
def logout():
    session.clear()
    return redirect("/business/login")


# 主页
@business_app.route("/index",endpoint="index")
@decorator.authentication
def index():
    systemName = dao.getSystemName()
    loginName = session.get("loginName")
    user = dao.selectBusinessUserByLoginName(loginName=loginName)
    content = {
        "systemName":systemName,
        "user":user
    }
    return render_template("manage/index.html",content=content)

# 首页
@business_app.route("/userFromRole",methods=["POST"],endpoint="userFromRole")
@decorator.authentication
def userFromRole():
    msg = {}
    msg["data"] = []
    option = {}
    option["color"] = ['#3398DB']
    option["title"] = {
                        "text": "角色成员分布",
                        "x":"center",
                        "y":"bottom"
    }
    option["tooltip"] = {
        "trigger": 'axis',
        "axisPointer": {
        "type": 'shadow'
        }
    }
    option["xAxis"] = []
    option["yAxis"] = [{"type":"value"}]
    option["series"] = []
    roleList = dao.selectBusinessRole()
    roleNameList = []
    userNumList = []
    for role in roleList:
        roleId = role.pk_id
        roleName = role.role_name
        roleNameList.append(roleName)
        userNum = models.db.session.query(models.BusinessUser).filter(models.BusinessUser.role_id==roleId,models.BusinessUser.delete_flag==0).count()
        userNumList.append(userNum)
    option["xAxis"].append({"type":"category","data":roleNameList})
    option["series"].append({"name":"人数","type":"bar","data":userNumList})
    msg["option"] = option
    msg["code"] = 0
    msg["msg"] = "请求成功！"
    return jsonify(msg)


@business_app.route("/menu",endpoint="menu")
@decorator.authentication
def menu():
    msg = {}
    msg["data"] = {}
    msg["data"]["list"] = []
    loginName = session.get("loginName")
    user = dao.selectBusinessUserByLoginName(loginName=loginName)
    userExtraResourceList = filter(None,user.extra_resource.split(","))
    userForbiddenResourceList = filter(None,user.forbidden_resource.split(","))
    roleResource = dao.selectBusinessRoleResourceByRoleId(roleId=user.role_id)
    resourceList = []
    extraResourceList = []
    forbiddenResourceList = []
    for roleResourceInfo in roleResource:
        roleResourceId = roleResourceInfo.resource_id
        resourceInfo = dao.selectBusinessResourceByResourceId(resourceId=roleResourceId)
        resourceList.append(resourceInfo.pk_id)
    for extraResourceId in userExtraResourceList:
        extraResource = dao.selectBusinessResourceByResourceId(resourceId=int(extraResourceId))
        extraResourceList.append(extraResource.pk_id)
    for forbiddenResourceId in userForbiddenResourceList:
        forbiddenResource = dao.selectBusinessResourceByResourceId(resourceId=int(forbiddenResourceId))
        forbiddenResourceList.append(forbiddenResource.pk_id)
    # 先求resourceList和extraResourceList的并集，再拿并集的结果去和forbiddenResourceList做差集
    rightResource = list(set(list(set(resourceList).union(set(extraResourceList)))).difference(set(forbiddenResourceList)))
    parentIdList = []
    for item in rightResource:
        info = dao.selectBusinessResourceByResourceId(resourceId=item)
        resourceId = info.pk_id
        resourceName = info.name
        resourceUrl = info.url
        resourceParent = info.parent
        if resourceParent not in parentIdList:
            parentResource = dao.selectBusinessResourceByResourceId(resourceId=resourceParent)
            parentIdList.append(resourceParent)
            appendInfo = {
                "id": parentResource.pk_id,
                "name": parentResource.name,
                "url": parentResource.url,
                "children": []
            }
            msg["data"]["list"].append(appendInfo)
        childrenAppendInfo = {
            "id": resourceId,
            "name": resourceName,
            "url": resourceUrl,
        }
        for childrenInfo in msg["data"]["list"]:
            if resourceParent == childrenInfo.get("id"):
                childrenInfo.get("children").append(childrenAppendInfo)
    return jsonify(msg)


@business_app.route("/roleManage",endpoint="roleManage")
@decorator.authentication
def roleManager():
    return render_template("manage/roleManage.html")

@business_app.route("/getRole",methods=["GET","POST"],endpoint="getRole")
@decorator.authentication
def getRole():
    msg = {}
    msg["data"] = []
    if request.method == "GET":
        params = request.args
        page = params.get("page")
        limit = params.get("limit")
        keyWords = params.get("keyWords")
        msg["count"] = models.db.session.query(models.BusinessRole).filter(models.BusinessRole.delete_flag==0,models.BusinessRole.role_name.like("%"+keyWords+"%") if keyWords is not None else "").count()
        roleObj = models.BusinessRole.query.filter(models.BusinessRole.delete_flag==0,models.BusinessRole.role_name.like("%"+keyWords+"%") if keyWords is not None else "")
        roleList = roleObj.paginate(page=int(page),per_page=int(limit)).items
        for role in roleList:
            appendInfo = {
                "roleId": role.pk_id,
                "roleName": role.role_name,
                "roleDes": role.role_des,
            }
            msg["data"].append(appendInfo)
        msg["code"] = 0
    else:
        roleList = dao.selectBusinessRole()
        for role in roleList:
            appendInfo = {
                "roleId": role.pk_id,
                "roleName": role.role_name
            }
            msg["data"].append(appendInfo)
        msg["code"] = 0
    return jsonify(msg)


@business_app.route("/addRole",methods=["GET","POST"],endpoint="addRole")
@decorator.authentication
def addRole():
    msg = {}
    msg["data"] = []
    if request.method == "GET":
        return render_template("manage/addRole.html")
    else:
        params = request.form
        roleName = params.get("roleName")
        roleDes = params.get("roleDes")
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        newRole = models.BusinessRole(role_name=roleName,role_des=roleDes,create_time=now,update_time=now)
        models.db.session.add(newRole)
        models.db.session.commit()
        msg["code"] = 0
        msg["msg"] = "请求成功！"
        return jsonify(msg)


@business_app.route("/updateRole",methods=["GET","POST"],endpoint="updateRole")
@decorator.authentication
def updateRole():
    msg = {}
    msg["data"] = []
    if request.method == "GET":
        params = request.args
        roleId = params.get("roleId")
        role = dao.selectBusinessRoleByRoleId(roleId=roleId)
        # 获取所有权限
        resourceList = dao.selectBusinessResource()
        resourceItems = []
        for resourceItem in resourceList:
            resourceId = resourceItem.pk_id
            resourceName = resourceItem.name
            resourceParent = resourceItem.parent
            if resourceParent == -1:
                appendInfo = {
                    "resourceId":resourceId,
                    "resourceName":resourceName,
                    "children": []
                }
                resourceItems.append(appendInfo)
            else:
                for parentInfo in resourceItems:
                    if resourceParent == parentInfo["resourceId"]:
                        appendChildrenInfo = {
                            "resourceId": resourceId,
                            "resourceName": resourceName,
                            "checked": False
                        }
                        parentInfo["children"].append(appendChildrenInfo)
                    else:
                        pass
        # 获取角色的权限列表，并标记已有权限
        roleResource = dao.selectBusinessRoleResourceByRoleId(roleId=roleId)
        roleResourceList = []
        for roleResourceItem in roleResource:
            roleResourceId = roleResourceItem.resource_id
            roleResourceList.append(roleResourceId)
        for item in resourceItems:
            roleResourceChildrenItems = item["children"]
            for roleResourceChildrenItem in roleResourceChildrenItems:
                if roleResourceChildrenItem["resourceId"] in roleResourceList:
                    roleResourceChildrenItem["checked"] = True
        content = {
            "roleId":role.pk_id,
            "roleDes":role.role_des,
            "roleName":role.role_name,
            "resourceList":resourceItems
        }
        return render_template("manage/updateRole.html", content=content)
    else:
        params = request.form
        roleId = params.get("roleId")
        roleDes = params.get("roleDes")
        # filter过滤resource列表中的空字符串
        resource = filter(None, params.get("resource").split(","))
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        # 获取角色信息，并更新角色描述
        role = dao.selectBusinessRoleByRoleId(roleId=roleId)
        role.role_des = roleDes
        role.update_time = now
        models.db.session.commit()
        # 先删除该角色所有的权限，再重新写入更新的权限
        if dao.deleteBusinessRoleResourceByRoleId(roleId=roleId):
            roleUsers = dao.selectBusinessUserByRoleId(roleId=roleId)
            resourceIdSet = set()
            for resourceId in resource:
                newResource = models.BusinessRoleResource(role_id=roleId,resource_id=int(resourceId),create_time=now,update_time=now)
                models.db.session.add(newResource)
                models.db.session.commit()
                resourceIdSet.add(resourceId)

            for user in roleUsers:
                extraResourceSet = set(filter(None,user.extra_resource.split(",")))
                forbiddenResourceSet = set(filter(None,user.forbidden_resource.split(",")))
                user.extra_resource = ",".join(list(extraResourceSet.difference(resourceIdSet)))
                user.forbidden_resource = ",".join(list(forbiddenResourceSet.intersection(resourceIdSet)))
                models.db.session.commit()


            msg["code"] = 0
            msg["msg"] = "修改成功！"
        else:
            msg["code"] = 1001
            msg["msg"] = "请求异常！"
        return jsonify(msg)


@business_app.route("/deleteRole",methods=["POST"],endpoint="deleteRole")
@decorator.authentication
def deleteRole():
    msg = {}
    msg["data"] = []
    params = request.form
    roleId = params.get("roleId")
    role = dao.selectBusinessRoleByRoleId(roleId=roleId)
    role.delete_flag = 1
    models.db.session.commit()
    msg["code"] = 0
    msg["msg"] = "删除成功！"
    return jsonify(msg)


@business_app.route("/userManage",endpoint="userManage")
@decorator.authentication
def userManager():
    return render_template("manage/userManage.html")


@business_app.route("/getUser",endpoint="getUser")
@decorator.authentication
def getUser():
    msg = {}
    msg["data"] = []
    params = request.args
    page = params.get("page")
    limit = params.get("limit")
    keyWords = params.get("keyWords")
    msg["count"] = models.db.session.query(models.BusinessUser).filter(models.BusinessUser.delete_flag == 0,models.BusinessUser.login_name.like("%"+keyWords+"%") if keyWords is not None else "").count()
    userObj = models.BusinessUser.query.filter(models.BusinessUser.delete_flag == 0,models.BusinessUser.login_name.like("%"+keyWords+"%") if keyWords is not None else "")
    userList = userObj.paginate(page=int(page), per_page=int(limit)).items
    for user in userList:
        appendInfo = {
            "userId": user.pk_id,
            "loginName": user.login_name,
            "nickName": user.nick_name,
        }
        msg["data"].append(appendInfo)
    msg["code"] = 0
    return jsonify(msg)



# 新增用户
@business_app.route("/addUser",methods=["GET","POST"],endpoint="addUser")
@decorator.authentication
def addUser():
    msg = {}
    msg["data"] = []
    if request.method == "GET":
        return render_template("manage/addUser.html")
    else:
        params = request.form
        loginName = params.get("loginName")
        nickName = params.get("nickName")
        roleId = params.get("role")
        if loginName and nickName and roleId:
            passWord = hashlib.md5("123456".encode("utf-8")).hexdigest()
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            if models.db.session.query(models.BusinessUser).filter(models.BusinessUser.login_name==loginName).first():
                msg["code"] = 1002
                msg["msg"] = "该账号已被注册！"
            else:
                newUser = models.BusinessUser(login_name=loginName,password=passWord,role_id=roleId,nick_name=nickName,create_time=now,update_time=now)
                models.db.session.add(newUser)
                models.db.session.commit()
                msg["code"] = 0
                msg["msg"] = "请求成功！"
        else:
            msg["code"] = 1001
            msg["msg"] = "请将数据填写完整！"
        return jsonify(msg)


# 编辑用户
@business_app.route("/updateUser",methods=["GET","POST"],endpoint="updateUser")
@decorator.authentication
def updateUser():
    msg = {}
    msg["data"] = []
    if request.method == "GET":
        params = request.args
        userId = params.get("userId")
        user = dao.selectBusinessUserByUserId(userId=userId)
        userExtraResourceList = filter(None,user.extra_resource.split(","))
        userForbiddenResourceList = filter(None,user.forbidden_resource.split(","))
        roleList = dao.selectBusinessRole()
        resourceList = dao.selectBusinessResource()
        roleResourceList = dao.selectBusinessRoleResourceByRoleId(roleId=user.role_id)

        roleResource = []
        # 遍历出所有的角色的resourceId
        for roleResourceInfo in roleResourceList:
            roleResource.append(roleResourceInfo.resource_id)

        # 遍历出所有的非角色权限
        extraResourceList = []
        forbiddenResourceList = []
        for resource in resourceList:
            # 如果business_resource.parent=-1
            if resource.parent == -1:
                extraResourceList.append({"resourceId":resource.pk_id,"resourceName":resource.name,"children":[]})
                forbiddenResourceList.append({"resourceId": resource.pk_id, "resourceName": resource.name, "children": []})
            else:
                # 如果resourceId不在角色权限里
                if resource.pk_id not in roleResource:

                    # 添加到上级权限的children中
                    for parentResource in extraResourceList:
                        if parentResource["resourceId"] == resource.parent:
                            extraResourceId = resource.pk_id
                            extraResourceName = resource.name
                            if str(extraResourceId) in userExtraResourceList:
                                checked = True
                            else:
                                checked = False
                            parentResource["children"].append({"resourceId":extraResourceId,"resourceName":extraResourceName,"checked":checked})
                else:
                    for parentResource in forbiddenResourceList:
                        if parentResource["resourceId"] == resource.parent:
                            forbiddenResourceId = resource.pk_id
                            forbiddenResourceName = resource.name
                            if str(forbiddenResourceId) in userForbiddenResourceList:
                                checked = True
                            else:
                                checked = False
                            parentResource["children"].append({"resourceId":forbiddenResourceId,"resourceName":forbiddenResourceName,"checked":checked})
        content = {
            "user":user,
            "roleList": roleList,
            "extraResourceList":extraResourceList,
            "forbiddenResourceList":forbiddenResourceList
        }
        return render_template("manage/updateUser.html",content=content)

    else:
        try:
            params = request.form
            userId = params.get("userId")
            loginName = params.get("loginName")
            nickName = params.get("nickName")
            roleId = params.get("roleId")
            extraResourceList = params.get("extraResourceList")
            forbiddenResourceList = params.get("forbiddenResourceList")
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            user = dao.selectBusinessUserByUserId(userId=userId)
            user.login_name = loginName
            user.nick_name = nickName
            user.role_id = roleId
            user.extra_resource = extraResourceList
            user.forbidden_resource = forbiddenResourceList
            user.update_time = now
            models.db.session.commit()
            msg["code"] = 0
            msg["msg"] = "保存成功！"
        except:
            msg["code"] = 1001
            msg["msg"] = "请求异常！"
        return jsonify(msg)

# 删除用户
@business_app.route("/deleteUser",methods=["POST"],endpoint="deleteUser")
@decorator.authentication
def deleteUser():
    msg = {}
    msg["data"] = []
    try:
        params = request.form
        userId = params.get("userId")
        user = dao.selectBusinessUserByUserId(userId=userId)
        user.delete_flag = 1
        models.db.session.commit()
        msg["code"] = 0
        msg["msg"] = "删除成功！"
    except:
        msg["code"] = 1001
        msg["msg"] = "请求异常！"
    return jsonify(msg)

@business_app.route("/systemConfigManage",endpoint="systemConfigManage")
@decorator.authentication
def systemConfigManage():
    return render_template("manage/systemConfigManage.html")

# 获取系统配置参数
@business_app.route("/getSystemConfig",endpoint="getSystemConfig")
@decorator.authentication
def getSystemConfig():
    msg = {}
    msg["data"] = []
    systemConfig = models.db.session.query(models.BusinessKeyWord).all()
    for item in systemConfig:
        appendInfo = {
            "keyWordId": item.pk_id,
            "key": item.key,
            "value": item.value,
            "des": item.des
        }
        msg["data"].append(appendInfo)
    msg["code"] = 0
    msg["msg"] = "请求成功"
    return jsonify(msg)

# 编辑系统配置参数
@business_app.route("/updateSystemConfig",methods=["GET","POST"],endpoint="updateSystemConfig")
@decorator.authentication
def updateSystemConfig():
    msg = {}
    msg["data"] = []
    if request.method == "GET":
        params = request.args
        keyWordId = params.get("keyWordId")
        keyWord = models.db.session.query(models.BusinessKeyWord).filter(models.BusinessKeyWord.pk_id==keyWordId).first()
        return render_template("manage/updateSystemConfig.html",content=keyWord)
    else:
        params = request.form
        keyWordId = params.get("keyWordId")
        value = params.get("value")
        des = params.get("des")
        keyWord = models.db.session.query(models.BusinessKeyWord).filter(models.BusinessKeyWord.pk_id==keyWordId).first()
        keyWord.value = value
        keyWord.des = des
        models.db.session.commit()
        msg["code"] = 0
        msg["msg"] = "保存成功！"
        return jsonify(msg)