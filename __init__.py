from flask import Flask

app = Flask(__name__)

from app.views import forum, general, post, thread, user, views, post
