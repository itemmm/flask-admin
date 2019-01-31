from flask import Flask,redirect
from manager.operator import business_app
from content.content import content_app
from test_manage.testManage import testManage_app
from models import db
from flask_session import Session
import redis





app = Flask(__name__)
app.register_blueprint(business_app, url_prefix="/business")
app.register_blueprint(content_app, url_prefix="/content")
app.register_blueprint(testManage_app,url_prefix="/testManage")


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@192.168.31.100:3306/business?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['SESSION_TYPE'] = 'redis'  # session类型为redis
app.config['SESSION_PERMANENT'] = False  # 如果设置为True，则关闭浏览器session就失效。
app.config['SESSION_USE_SIGNER'] = False  # 是否对发送到浏览器上session的cookie值进行加密
app.config['SESSION_KEY_PREFIX'] = 'session:'  # 保存到session中的值的前缀
app.config['SESSION_REDIS'] = redis.Redis(host='192.168.31.60', port='6379')  # 用于连接redis的配置
app.config['PERMANENT_SESSION_LIFETIME'] = 3600 #session长期有效，则设定session生命周期，整数秒，默认大概不到3小时。
Session(app)


db.init_app(app)


@app.route("/")
def index():
    return redirect("/business/index")


if __name__ == '__main__':
    app.run(debug=True,host="192.168.31.102")