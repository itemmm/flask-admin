import models




def getSystemName():
    systemName = models.db.session.query(models.BusinessKeyWord).filter(models.BusinessKeyWord.key=="systemName").first()
    return systemName



# 获取所有的权限信息
def selectBusinessResource():
    resource = models.db.session.query(models.BusinessResource).all()
    return resource

# 通过roleId获取该角色所有的权限
def selectBusinessResourceByRoleId(roleId):
    resource = models.db.session.query(models.BusinessRoleResource).filter(models.BusinessRoleResource.role_id==roleId).all()
    return resource

# 根据权限Id获取权限信息
def selectBusinessResourceByResourceId(resourceId):
    resource = models.db.session.query(models.BusinessResource).filter(models.BusinessResource.pk_id==resourceId).first()
    return resource

# 获取所有的角色信息
def selectBusinessRole():
    role = models.db.session.query(models.BusinessRole).filter(models.BusinessRole.delete_flag==0).all()
    return role

# 根据角色Id获取角色信息
def selectBusinessRoleByRoleId(roleId):
    role = models.db.session.query(models.BusinessRole).filter(models.BusinessRole.pk_id==roleId).first()
    return role

def selectBusinessUserByRoleId(roleId):
    users = models.db.session.query(models.BusinessUser).filter(models.BusinessUser.role_id==roleId).all()
    return users

# 根据角色Id获取角色的所有权限信息
def selectBusinessRoleResourceByRoleId(roleId):
    resource = models.db.session.query(models.BusinessRoleResource).filter(models.BusinessRoleResource.role_id==roleId).all()
    return resource

# 根据roleId删除所有权限
def deleteBusinessRoleResourceByRoleId(roleId):
    try:
        models.db.session.query(models.BusinessRoleResource).filter(models.BusinessRoleResource.role_id==roleId).delete()
        return True
    except:
        return False

# 根据loginName获取用户
def selectBusinessUserByLoginName(loginName):
    user = models.db.session.query(models.BusinessUser).filter(models.BusinessUser.login_name==loginName,models.BusinessUser.delete_flag==0).first()
    return user

# 通过userId获取用户
def selectBusinessUserByUserId(userId):
    user = models.db.session.query(models.BusinessUser).filter(models.BusinessUser.pk_id==userId,models.BusinessUser.delete_flag==0).first()
    return user