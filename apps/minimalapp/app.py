import logging
import os

from email_validator import EmailNotValidError, validate_email
from flask import (
    Flask,
    current_app,
    flash,
    g,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

# 서버 프로그램 객체를 만든다.
# __name__실행중인 모듈의 시스템 상의 이름
app = Flask(__name__)
app.config["SECRET_KEY"]="2AZSMss3p5QPbcY2hBsJ"
app.logger.setLevel(logging.DEBUG)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

#Mail 클래스의 config 추가
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

toolbar=DebugToolbarExtension(app)


mail = Mail(app)

# 기본주소로 요청이 왔을 때 무엇을 정의하기
@app.route('/')
def index():
	return 'Hello, flask'

@app.route('/hello/<name>', methods=["GET"], endpoint="hello-endpoint")
def hello(name):
	# return 'Hello, World'
    return f'Hi, {name}'

@app.route('/name/<name>')
def show_name(name):
      return render_template("index.html", name=name)

with app.test_request_context():
      print(url_for("index"))
      print(url_for("hello-endpoint", name="w"))
      print(url_for("show_name", name="j", page="1"))

ctx = app.app_context()
ctx.push()
print(current_app.name)
g.connection = "connection"
print(g.connection)

with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))

@app.route("/contact")
def contact():
      return render_template("contact.html")
      response = make_response(render_template("contact.html"))
      response.set_cookie("flaskbook key", "flaskbook value")
      session["username"] = "ichiro"
      return response

@app.route("/contact/complete", methods=["GET","POST"])
def contact_complete():
      if request.method=="POST":
            username = request.form["username"]
            email = request.form["email"]
            description = request.form["description"]

            is_valid = True

            if not username:
                  flash("사용자명은 필수입니다")
                  is_valid = False

            if not email:
                  flash("메일주소는 필수입니다")
                  is_valid = False

            try:
                  validate_email(email)
            except EmailNotValidError:
                  flash("메일 주소의 형식으로 입력해주세요")
                  is_valid = False

            if not description:
                  flash("문의 내용은 필수입니다")
                  is_valid = False

            if not is_valid:
                  return redirect(url_for("contact"))

            
            send_email(
                  email,
                  "문의 쌩유",
                  "contact_mail",
                  username=username,
                  description=description,
            )

            flash("문의내용이 발송되었습니다")
            return redirect(url_for("contact_complete"))
      
      return render_template("contact_complete.html")

app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


# if __name__ == '__main':
# 	app.run(debug = true)