import os   #added
from flask import Flask

app = Flask(__name__, instance_path=os.getcwd(),template_folder='../template') 