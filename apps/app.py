from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    # app.register_blueprint(sample, url_prefix="/sample", subdomain="example")
    # app.register_blueprint(sample, url_prefix="/sample2")
    # crud = Blueprint("crud", __name__, template_folder="templates")

    return app

# sample=Blueprint(
#     __name__,
#     "sample",
#     static_folder="static",
#     template_folder="template",
#     url_prefix="/sample",
#     subdomain="example",
# )
   