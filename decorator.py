from flask import redirect,session
import models




# 用于判断用户是否登录
def authentication(func):
    def wrapper(*args,**kwargs):
        # 从session里获取login_name和password
        loginName = session.get("loginName")
        passWord = session.get("passWord")
        # 根据login_name查找用户
        user = models.db.session.query(models.BusinessUser).filter(models.BusinessUser.login_name==loginName,models.BusinessUser.delete_flag==0).first()
        # 如果没有查找到这个用户
        if user is None:
            # 重定向至登录页面
            return redirect("/business/login")
        else:
            # 如果loginName和passWord和数据库的一致
            if loginName==user.login_name and passWord==user.password:
                # 不做处理
                return func(*args,**kwargs)
            else:
                # 不一致则重定向至登录页面
                return redirect("/business/login")
    return wrapper