from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class BusinessResource(db.Model):
    __tablename__ = "business_resource"
    pk_id = db.Column(db.INTEGER,primary_key=True,autoincrement=True,nullable=False)
    name = db.Column(db.VARCHAR(255))
    url = db.Column(db.VARCHAR(255))
    parent = db.Column(db.VARCHAR(255))
    delete_flag = db.Column(db.INTEGER,default=0)
    create_time = db.Column(db.DATETIME)
    update_time = db.Column(db.DATETIME)


class BusinessRole(db.Model):
    __tablename__ = "business_role"
    pk_id = db.Column(db.INTEGER, primary_key=True,autoincrement=True,nullable=False)
    role_name = db.Column(db.VARCHAR(255))
    role_des = db.Column(db.VARCHAR(255))
    delete_flag = db.Column(db.INTEGER,default=0)
    create_time = db.Column(db.DATETIME)
    update_time = db.Column(db.DATETIME)


class BusinessRoleResource(db.Model):
    __tablename__ = "business_role_resource"
    pk_id = db.Column(db.INTEGER, primary_key=True,autoincrement=True,nullable=False)
    role_id = db.Column(db.INTEGER)
    resource_id = db.Column(db.INTEGER)
    create_time = db.Column(db.DATETIME)
    update_time = db.Column(db.DATETIME)

class BusinessUser(db.Model):
    __tablename__ = "business_user"
    pk_id = db.Column(db.INTEGER, primary_key=True,autoincrement=True,nullable=False)
    login_name = db.Column(db.VARCHAR(255))
    password = db.Column(db.VARCHAR(255))
    nick_name = db.Column(db.VARCHAR(255))
    role_id = db.Column(db.INTEGER)
    extra_resource = db.Column(db.VARCHAR(255),default="")
    forbidden_resource = db.Column(db.VARCHAR(255),default="")
    delete_flag = db.Column(db.INTEGER,default=0)
    create_time = db.Column(db.DATETIME)
    update_time = db.Column(db.DATETIME)


class BusinessKeyWord(db.Model):
    __tablename__ = "business_keyword"
    pk_id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    key = db.Column(db.VARCHAR(255))
    value = db.Column(db.VARCHAR(255))
    des = db.Column(db.VARCHAR(255))



class ContentFile(db.Model):
    __tablename__ = "content_file"
    pk_id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.VARCHAR(255))
    parent = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    des = db.Column(db.TEXT)
    delete_flag = db.Column(db.INTEGER,default=0)
    create_time = db.Column(db.DATETIME)
    update_time = db.Column(db.DATETIME)