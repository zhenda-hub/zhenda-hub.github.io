+++
title = 'Flask Tutorial'
subtitle = ""
date = 2024-05-26T01:17:16+08:00
draft = false
toc = true
tags = ['web']
+++

link: <https://flask.palletsprojects.com/en/stable/>

## 快速开始

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

### 其他有用函数

```python
from flask import request, url_for, render_template, abort, redirect, make_response, session


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'
```

## app.config

<https://flask.palletsprojects.com/en/stable/config/#configuration-basics>

实际上是字典的子类， 可以像任何字典一样进行修改

An interesting pattern is also to use classes and inheritance for configuration:

```python
class Config(object):
    TESTING = False

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DATABASE_URI = "sqlite:////tmp/foo.db"

class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

app.config.from_object('configmodule.ProductionConfig')
```

## view类

```python
from flask.views import View

class ListView(View):
    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        items = self.model.query.all()
        return render_template(self.template, items=items)

app.add_url_rule(
    "/users/",
    view_func=ListView.as_view("user_list", User, "users.html"),
)
app.add_url_rule(
    "/stories/",
    view_func=ListView.as_view("story_list", Story, "stories.html"),
)
```

## 中间件

<https://flask.palletsprojects.com/en/stable/lifecycle/>

```python
@app.before_request
@app.after_request
@app.teardown_request
```

## 常用扩展

```bash
pip install Flask-SQLAlchemy
pip install Flask-Migrate
pip install WTForms
pip install Flask-WTF
pip install Flask-Admin

pip install Flask-Login
```
