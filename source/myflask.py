from flask import *
from flask import Flask


from flask import Flask
from webpy.login import login_bp, login_manager

app = Flask(__name__)
app.secret_key = "d5av5h6s2f5sa5c1za56ad1fgr5w6aa1v5aa6S55"
login_manager.init_app(app)
# 登录功能

from webpy.ip import ip_info
app.register_blueprint(ip_info)
app.register_blueprint(login_bp)


if __name__ == "__main__":
    app.run(debug=True)