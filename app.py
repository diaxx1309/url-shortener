from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import string,random

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///urls.db'
db= SQLAlchemy(app)

class URL(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    code=db.Column(db.String(50), unique=True , nullable=False)
    long_url=db.Column(db.String(500), nullable= False)
    clicks=db.Column(db.Integer, default=0)

def generate_short():
    return ''.join(random.choices(string.ascii_letters+string.digits,k=6))

@app.route('/',methods=['GET','POST'])
def index():
    short_url=None
    if request.method=='POST':
        long_url=request.form['long_url']
        if not long_url.startswith(('http://','https://')):
            long_url='https://'+long_url
        alias= request.form.get('alias')
        if alias:
            existing=URL.query.filter_by(code=alias).first()
            if existing:
                code=generate_short()
            else:
                code=alias
        else:
            code=generate_short()
        new_url= URL(code=code , long_url=long_url)
        db.session.add(new_url)
        db.session.commit()
        short_url=request.host_url+code
    all_urls=URL.query.all()
    return render_template('index.html',short_url=short_url,all_urls=all_urls)

@app.route('/<code>')
def redirect_url(code):
    url_entry= URL.query.filter_by(code=code).first()
    if url_entry:
        url_entry.clicks+=1
        db.session.commit()
        return redirect(url_entry.long_url)
    return "URL NOT FOUND",404

@app.route('/delete/<int:id>')
def delete_url(id):
    url=URL.query.get(id)
    if url:
        db.session.delete(url)
        db.session.commit()
    return redirect('/')

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)