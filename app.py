from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    articles = Article.query.all()
    return render_template('home.html', articles=articles)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_article = Article(title=title, description=description)
        db.session.add(new_article)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
