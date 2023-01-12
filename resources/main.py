import os   #added
from flask import render_template ,redirect,url_for
from flask_security import Security, SQLAlchemyUserDatastore,login_required,logout_user
from flask_smorest import Api
from utils.db import db    
from models import user
from views.disease import blp as DiseaseBlueprint
from views.patient import blp as PatientBlueprint
from views.symptom import blp as SymptomBlueprint
from views.user import blp as UserBlueprint
from views.login import blp as LoginBlueprint
from views.signup import blp as SignupBlueprint
from security.confirm_email import blp as ConfirmEmailBluePrint
from security.unconfirmed import blp as UnconfirmedBlueprint
from security.authorization_token import token_required
from utils.login_manager import login_manager
from utils.mail import mail
from utils.app import app as application
from utils.beforeFirstRequest import before_first_request

def create_app(db_url=None):
    
    app = application
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Symptoms Checker REST API"
    app.config["API_VERSION"] = "v1.0.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
            "OPENAPI_SWAGGER_UI_URL"
        ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECURITY_PASSWORD_SALT'] = 'some arbitrary super secret string'
    app.config['SECRET_KEY'] = 'super-secret'
    
    app.config['MAIL_SERVER']='smtp.gmail.com' 
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'tbs.montassar.chihi@gmail.com'
    app.config['MAIL_PASSWORD'] = 'hhidbcglxkmgcqxg'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    
    db.init_app(app)
    db.session.expire_on_commit = False
    mail.init_app(app)
    login_manager.init_app(app)
    
    @app.route('/')
    def index():
        return render_template("index.html")
    
    @login_manager.user_loader
    def load_user(id):
        return user.User.query.get(int(id))
    
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/")
    
    api = Api(app)
    api.register_blueprint(SignupBlueprint)
    api.register_blueprint(ConfirmEmailBluePrint)
    api.register_blueprint(LoginBlueprint)
    api.register_blueprint(UnconfirmedBlueprint)
    api.register_blueprint(DiseaseBlueprint)
    api.register_blueprint(PatientBlueprint)
    api.register_blueprint(SymptomBlueprint)
    api.register_blueprint(UserBlueprint)

    user_datastore = SQLAlchemyUserDatastore(db, user.User,user.Role)
    security = Security(app, user_datastore)
    
    @app.before_first_request
    def create_tables():
        before_first_request(user_datastore)
    
    return app

app = create_app()