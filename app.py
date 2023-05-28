from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# создаем объект класса
# пеердаем в класс Flask название файла
# основной файл для работы с классом Flask — __name__, то есть app.py
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # когда будем выбирать какой-либо объект на основе класса,
    # нам будет выдаваться этот объект и его айди
    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# @app.route('/user/<string:name>/<int:id>')
# def user(name, id):
#     return "User page " + name + " " + str(id)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def posts_read(id):
    article = Article.query.get(id)
    return render_template('posts_read.html', article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'при удалении статьи возникла ошибка'


@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        return render_template('post_update.html', article=article)


@app.route('/create_article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            # добавляем объект в БД
            db.session.add(article)
            # сохраняем объект в БД
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create_article.html')

with app.app_context():
    # Create the database tables
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)