from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title,body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['GET'])
def main():
    title = request.args.get('title')
    body = request.args.get('body')
    if request.args:
       blog_id = request.args.get("id")
       blog = Blog.query.get(blog_id)

       return render_template('singleblog.html', blog=blog)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html',blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def index():
    title_error = ''
    body_error = ''
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']

        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')

    return render_template('newpost.html',title_error=title_error,body_error=body_error)
    

if __name__ == '__main__':
    app.run()